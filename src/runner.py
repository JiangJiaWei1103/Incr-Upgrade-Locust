#!/usr/bin/env python3
"""
Automated rollback load testing orchestrator for KubeRay RayService incremental upgrade.

Usage:
    cd rollback/
    python orchestrator.py --scenario scenarios/p0_basic_rollback.yaml

    # Skip deploy if RayService already running:
    python orchestrator.py --scenario scenarios/p0_basic_rollback.yaml --no-deploy

    # Override Gateway host (e.g., via port-forward):
    python orchestrator.py --scenario scenarios/p0_basic_rollback.yaml --host http://localhost:8080

Prerequisites:
    - Kind cluster with Istio + MetalLB ready (run setup.sh)
    - kubectl configured to access the cluster
    - pip install locust pyyaml requests
"""

import argparse
from re import L
import signal
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

import yaml

from utils import RayServiceClient, StatusLogger, StatusChecker, get_locust_rps, extract_status


class Runner:
    """Coordinates upgrade/rollback load testing."""

    GATEWAY_LOCAL_PORT = 8080
    GATEWAY_REMOTE_PORT = 80
    LOCUST_WEB_PORT = 8089
    PRINT_INTERVAL = 3

    def __init__(self, scenario: str, host: str | None = None, deploy_rayservice: bool = False) -> None:
        self.base_dir = Path(__file__).resolve().parent

        with open(scenario) as f:
            self.scenario = yaml.safe_load(f)
        self.rs_cfg = self.scenario["rayservice"]
        self.locust_cfg = self.scenario["locust"]
        self.actions = self.scenario["actions"]
        self.completion = self.scenario["completion"]
        self.timeouts = self.scenario["timeouts"]

        self.host = host
        self.deploy_rayservice = deploy_rayservice

        self._setup()

    def _setup(self) -> None:
        self.output_dir = self.base_dir / "outputs" / self.scenario["name"]
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.client = RayServiceClient(
            self.rs_cfg.get("namespace", "default"),
            self.rs_cfg["name"],
        )
        self.logger = StatusLogger(self.output_dir / "status_log.csv")
        self.checker = StatusChecker()

        self.locust_proc = None
        self.port_forward_proc = None
        self.phase = "init"
        self._last_print = 0

    def run(self) -> None:
        try:
            if self.deploy_rayservice:
                self._deploy()
            self._wait_for_ready()
            # self._resolve_host()
            self._port_forward_gateway()
            self._start_locust()
            self._wait_for_warmup()
            self._run_actions()
            self._wait_for_completion()
            self._summary()
        except KeyboardInterrupt:
            print("\n[runner] Interrupted.")
        except Exception as exc:
            print(f"\n[runner] ERROR: {exc}")
            raise
        finally:
            self._cleanup()

    def _deploy(self) -> None:
        yaml_path = self.base_dir / self.rs_cfg["yaml"]
        print(f"[runner] Deploying RayService from {yaml_path}")
        self.client.apply(str(yaml_path))
        self.phase = "deploying"

    def _wait_for_ready(self) -> None:
        print("[runner] Waiting for RayService ready...")
        ddl = time.time() + self.timeouts["rayservice_ready"]

        while time.time() < ddl:
            rs = self.client.get()
            if rs is not None:
                st = extract_status(rs)
                self.logger.log("wait_for_rs_ready", st)
                if st and st["ready"] and not st["upgrading"]:
                    print(f"[runner] Ready. Active cluster: {st['active_cluster']}")
                    self.phase = "ready"
                    return
            time.sleep(2)

        raise TimeoutError("RayService not ready in time")

    # def _resolve_host(self):
    #     if self.host:
    #         print(f"[runner] Using host: {self.host}")
    #         return

    #     ip = self.client.get_gateway_ip()
    #     if ip:
    #         self.host = f"http://{ip}"
    #         print(f"[runner] Resolved Gateway IP: {self.host}")
    #     else:
    #         raise RuntimeError(
    #             "Cannot resolve Gateway IP. Use --host or set up port-forward."
    #         )

    def _port_forward_gateway(self) -> None:
        parsed = urlparse(self.host or "")
        if parsed.hostname not in ("localhost", "127.0.0.1"):
            return

        local_port = parsed.port or self.GATEWAY_LOCAL_PORT 
        print(f"[runner] Starting port-forward svc/{self.rs_cfg['name']}-gateway-istio {local_port}:{self.GATEWAY_REMOTE_PORT}")
        self.port_forward_proc = self.client.port_forward_gateway(local_port, self.GATEWAY_REMOTE_PORT)
        time.sleep(1)

    def _start_locust(self) -> None:
        lc = self.locust_cfg
        locustfile = str(self.base_dir / lc["locustfile"])
        web_port = lc.get("web_port", self.LOCUST_WEB_PORT)

        cmd = [
            "locust",
            "-f", locustfile,
            "--host", self.host,
            "--users", str(lc["users"]),
            "--spawn-rate", str(lc["spawn_rate"]),
            "--csv", str(self.output_dir / "locust"),
            "--csv-full-history",
            "--autostart",
            "--web-port", str(web_port),
        ]
        print(f"[runner] Starting Locust (UI at http://localhost:{web_port})")
        self.locust_proc = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.phase = "warmup"

    def _wait_for_warmup(self) -> None:
        lc = self.locust_cfg
        threshold = lc["warmup_rps"]
        window = lc["warmup_stable_seconds"]
        web_port = lc.get("web_port", self.LOCUST_WEB_PORT)

        print(f"[runner] Warming up Locust (RPS >= {threshold} for {window}s)...")
        timeout = self.timeouts["locust_warmup"]
        ddl = time.time() + timeout
        stable = 0

        while time.time() < ddl:
            rs = self.client.get()
            if rs is not None:
                self.logger.log("locust_warmup", extract_status(rs))

            rps = get_locust_rps(web_port)
            if rps is not None and rps >= threshold:
                stable += 1
                if stable >= window:
                    print(f"[runner] Locust warmup done. RPS={rps:.0f}")
                    return
            else:
                stable = 0
            time.sleep(1)

        raise TimeoutError(f"Locust warmup timed out after {timeout:.2f}s")

    def _run_actions(self) -> None:
        for i, action in enumerate(self.actions):
            name = action["name"]
            print(f"\n[runner] === Action {i+1}/{len(self.actions)}: {name} ===")

            # Wait for trigger condition to be met.
            self._wait_for_trigger(name, action.get("when"))

            # Change RayService cluster spec to trigger upgrade/rollback.
            # TODO(jwj): Need to modify serve config to distinguish between old and new serve applications. 
            cpu = action["worker_cpu"]
            print(f"[runner] Setting worker CPU to {cpu}")
            self.client.put(cpu)

            if name == "rollback":
                self.phase = "rolling_back"
            elif name == "upgrade":
                self.phase = "upgrading"

            print(f"[runner] '{name}' triggered.")

    def _wait_for_trigger(self, action_name: str, condition: dict | None = None) -> None:
        # "warmed_up" triggers upgrade immediately since warmup already completed.
        # TODO(jwj): Seems redundant. Remove this condition. "warmed_up" must correspond to upgrade.
        # if condition == "warmed_up":
        #     return
        if condition is None:
            return

        timeout = self.timeouts["action"]
        ddl = time.time() + timeout
        web_port = self.locust_cfg.get("web_port", self.LOCUST_WEB_PORT)

        while time.time() < ddl:
            rs = self.client.get()
            if rs is None:
                time.sleep(1)
                continue

            elapsed = self.logger.elapsed()
            st = extract_status(rs)
            self.logger.log(self.phase, st)

            if st.get("rolling_back") and not self.checker.active:
                self.checker.start(st)
            if self.checker.active:
                self.checker.check(st, elapsed)

            self._print_line(st, elapsed, web_port)
            if self._condition_met(condition, st):
                return

            time.sleep(1)

        raise TimeoutError(f"Trigger for '{action_name}' timed out after {timeout:.2f}s")

    def _wait_for_completion(self) -> None:
        timeout = self.timeouts["completion"]
        ddl = time.time() + timeout
        web_port = self.locust_cfg.get("web_port", self.LOCUST_WEB_PORT)

        print(f"\n[runner] === Waiting for completion ===")
        while time.time() < ddl:
            rs = self.client.get()
            if rs is None:
                time.sleep(1)
                continue

            elapsed = self.logger.elapsed()
            st = extract_status(rs)
            self.logger.log(self.phase, st)

            if st.get("rolling_back") and not self.checker.active:
                self.checker.start(st)
            if self.checker.active:
                self.checker.check(st, elapsed)

            self._print_line(st, elapsed, web_port)
            if self._completion_met(self.completion, st):
                print(f"\n[runner] Completed at {elapsed:.2f}s")
                self.phase = "complete"
                self.logger.log("complete", st)
                return

            time.sleep(1)

        raise TimeoutError(f"Completion timed out after {timeout:.2f}s")

    @staticmethod
    def _condition_met(condition: dict, st: dict) -> bool:
        if len(condition) == 0:
            raise ValueError("Must specify at least one condition")
        
        for key, val in condition.items():
            if key == "pending_trp_gte":
                v = st.get("pending_trp")
                if v is None or v < val:
                    return False
            else:
                # TODO(jwj): Support more condition keys.
                raise ValueError(f"Unknown condition key: {key}")

        return True

    @staticmethod
    def _completion_met(completion: dict, st: dict) -> bool:
        if not (
            not st.get("upgrading")
            and not st.get("rolling_back")
            and st.get("pending_cluster") == ""
        ):
            return False

        # TODO(jwj): Support more completion keys.
        if "active_trp" in completion and st.get("active_trp") != completion["active_trp"]:
            return False

        return True

    def _print_line(self, st: dict, elapsed: float, web_port: int) -> None:
        if elapsed - self._last_print < self.PRINT_INTERVAL:
            return
        self._last_print = elapsed

        # The status dict must have these four fields.
        # We preserve falsy values (e.g., None, 0) as is.
        a_tc = st.get("active_tc", "?")
        a_trp = st.get("active_trp", "?")
        p_tc = st.get("pending_tc", "-")
        p_trp = st.get("pending_trp", "-")

        flags = []
        if st.get("upgrading"):
            flags.append("UPG")
        if st.get("rolling_back"):
            flags.append("RB")

        rps = get_locust_rps(web_port)
        rps_s = f"{rps:.0f}" if rps else "?"

        print(
            f"  [{elapsed:>6.1f}s] {self.phase:<12} | "
            f"Active TC={str(a_tc):>3} TRP={str(a_trp):>3} | "
            f"Pending TC={str(p_tc):>3} TRP={str(p_trp):>3} | "
            f"RPS={rps_s:>4} | {' '.join(flags)}"
        )

    def _summary(self):
        duration = time.time() - self.logger.start_time
        passed = not self.checker.violations
        label = "PASS" if passed else "FAIL"
        print(f"\n{'='*65}")
        print(f"  SCENARIO : {self.scenario['name']}")
        print(f"  RESULT   : {label}")
        print(f"  DURATION : {duration:.2f}s")
        print(f"  RESULTS  : {self.output_dir}/")
        if len(self.checker.violations) > 0:
            print(f"\n BEHAVIOR VIOLATIONS ({len(self.checker.violations)}):")
            for v in self.checker.violations:
                print(f"    - {v}")
        else:
            print(f"\n  All monotonicity invariants passed.")
        print(f"{'='*65}")

    def _cleanup(self):
        self.logger.close()
        if self.locust_proc is not None and self.locust_proc.poll() is None:
            print("[runner] Stopping Locust (SIGINT)...")
            self.locust_proc.send_signal(signal.SIGINT)
            try:
                self.locust_proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.locust_proc.kill()
        if self.port_forward_proc is not None and self.port_forward_proc.poll() is None:
            print("[runner] Stopping kubectl port-forward...")
            self.port_forward_proc.send_signal(signal.SIGINT)
            try:
                self.port_forward_proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.port_forward_proc.kill()
        if self.deploy_rayservice:
            print("[runner] Deleting RayService...")
            self.client.delete()


def main():
    parser = argparse.ArgumentParser(
        description="Automated runner for coordinating upgrade/rollback load testing",
    )
    parser.add_argument(
        "--scenario", required=True,
        help="Path to scenario YAML (e.g., scenarios/p0_basic_rollback.yaml)",
    )
    parser.add_argument(
        "--host",
        help="Override Locust target host (e.g., http://localhost:8080)",
        default="http://localhost:8080",
    )
    parser.add_argument(
        "--deploy-rayservice", action="store_true",
        help="Deploy RayService before running the load test",
    )
    args = parser.parse_args()

    runner = Runner(
        scenario=args.scenario,
        host=args.host,
        deploy_rayservice=args.deploy_rayservice,
    )
    runner.run()


if __name__ == "__main__":
    main()
