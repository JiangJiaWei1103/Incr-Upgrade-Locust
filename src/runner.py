#!/usr/bin/env python3
"""
This script is used to run load testing for incremental upgrade/rollback of KubeRay RayService.

Usage:
    # Setup environment.
    ./setup.sh

    # Run load testing.
    cd src/
    python3 runner.py --scenario scenarios/example.yaml --deploy-rayservice
"""

import argparse
import logging
import signal
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urlparse

import yaml

from utils import RayServiceClient, oomkill_head_pod, wait_for_oomkilled, StatusWriter, StatusChecker, get_locust_rps, extract_status, CustomFormatter


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

        # Setup runner logger.
        self.logger = logging.getLogger(f"runner.{id(self)}")
        self.logger.handlers.clear()
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        _fh = logging.FileHandler(self.output_dir / "runner.log", encoding="utf-8")
        _fh.setFormatter(CustomFormatter())
        self.logger.addHandler(_fh)
        _sh = logging.StreamHandler(sys.stdout)
        _sh.setFormatter(CustomFormatter())
        self.logger.addHandler(_sh)

        self.client = RayServiceClient(
            self.rs_cfg.get("namespace", "default"),
            self.rs_cfg["name"],
            logger=self.logger,
        )
        self.st_writer = StatusWriter(self.output_dir / "status_log.csv")
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
            self._port_forward_gateway()
            self._start_locust()
            self._wait_for_warmup()
            self._run_actions()
            self._wait_for_completion()
            self._check_rayservice_spec()
            self._summary()
        except KeyboardInterrupt:
            self.logger.info("\n[runner] Interrupted.")
        except Exception as exc:
            self.logger.error("\n[runner] ERROR: %s", exc)
            raise
        finally:
            self._cleanup()

    def _deploy(self) -> None:
        yaml_path = self.base_dir / self.rs_cfg["yaml"]
        self.logger.info("[runner] Deploying RayService from %s", yaml_path)
        self.client.apply(str(yaml_path))
        self.phase = "deploying"

    def _wait_for_ready(self) -> None:
        self.logger.info("[runner] Waiting for RayService ready...")
        ddl = time.time() + self.timeouts["rayservice_ready"]

        while time.time() < ddl:
            rs = self.client.get()
            if rs is not None:
                st = extract_status(rs)
                self.st_writer.write_row("wait_for_rs_ready", st)
                if st and st["ready"] and not st["upgrading"]:
                    self.logger.info("[runner] Ready. Active cluster: %s", st["active_cluster"])
                    self.phase = "ready"
                    return
            time.sleep(2)

        raise TimeoutError("RayService not ready in time")

    def _port_forward_gateway(self) -> None:
        parsed = urlparse(self.host or "")
        if parsed.hostname not in ("localhost", "127.0.0.1"):
            return

        local_port = parsed.port or self.GATEWAY_LOCAL_PORT 
        self.logger.info(
            "[runner] Starting port-forward svc/%s-gateway-istio %s:%s",
            self.rs_cfg["name"], local_port, self.GATEWAY_REMOTE_PORT,
        )
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
        self.logger.info("[runner] Starting Locust (UI at http://localhost:%s)", web_port)
        self.locust_proc = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        self.phase = "warmup"

    def _wait_for_warmup(self) -> None:
        lc = self.locust_cfg
        threshold = lc["warmup_rps"]
        window = lc["warmup_stable_seconds"]
        web_port = lc.get("web_port", self.LOCUST_WEB_PORT)

        self.logger.info("[runner] Warming up Locust (RPS >= %s for %ss)...", threshold, window)
        timeout = self.timeouts["locust_warmup"]
        ddl = time.time() + timeout
        stable = 0

        while time.time() < ddl:
            rs = self.client.get()
            if rs is not None:
                self.st_writer.write_row("locust_warmup", extract_status(rs))

            rps = get_locust_rps(web_port, self.logger)
            if rps is not None and rps >= threshold:
                stable += 1
                if stable >= window:
                    self.logger.info("[runner] Locust warmup done. RPS=%.0f", rps)
                    return
            else:
                stable = 0
            time.sleep(1)

        raise TimeoutError(f"Locust warmup timed out after {timeout:.2f}s")

    def _run_actions(self) -> None:
        for i, action in enumerate(self.actions):
            name = action["name"]
            self.logger.info("\n[runner] === Action %s/%s: Waiting for %s ===", i + 1, len(self.actions), name)

            # Wait for trigger condition to be met.
            self._wait_for_trigger(name, action.get("when"))

            # Change RayService cluster spec to trigger upgrade/rollback.
            # TODO(jwj): Need to modify serve config to distinguish between old and new serve applications. 
            cpu = action.get("worker_cpu")
            if name == "oomkill":
                assert cpu is None, f"oomkill do not need worker CPU change"
                self.logger.info("[runner] Crash the pending head Pod with OOMKilled")
                st = extract_status(self.client.get())
                # TODO(jwj): Do not hard code namespace here.
                oomkill_head_pod(st["pending_cluster"], logger=self.logger)
                wait_for_oomkilled(st["pending_cluster"], logger=self.logger)
            else:
                self.logger.info("[runner] Setting worker CPU to %s", cpu)
                self.client.put(cpu)

            if name == "upgrade":
                self.phase = "upgrading"
            elif name == "rollback":
                self.phase = "rolling_back"
            elif name == "cancel_rollback":
                # Resume upgrading.
                self.phase = "canceling_rollback"

            self.logger.info("[runner] '%s' triggered.", name)

    def _wait_for_trigger(self, action_name: str, condition: dict | None = None) -> None:
        if condition is None:
            # No condition means "warmed_up", which triggers upgrade immediately since warmup already completed.
            return

        timeout = self.timeouts["action"]
        ddl = time.time() + timeout
        web_port = self.locust_cfg.get("web_port", self.LOCUST_WEB_PORT)

        while time.time() < ddl:
            rs = self.client.get()
            if rs is None:
                time.sleep(1)
                continue

            elapsed = self.st_writer.elapsed()
            st = extract_status(rs)
            self.st_writer.write_row(self.phase, st)

            # Validate monotonicity during rollback.
            if st.get("rolling_back"):
                if not self.checker.active:
                    self.checker.start(st)
                else:
                    self.checker.check(st, elapsed)

            self._print_line(st, elapsed, web_port)
            if self._condition_met(condition, st):
                # Deactivation is idempotent.
                self.checker.stop()
                self._print_line(st, elapsed, web_port, finalized=True)
                return

            time.sleep(1)

        raise TimeoutError(f"Trigger for '{action_name}' timed out after {timeout:.2f}s")

    def _wait_for_completion(self) -> None:
        timeout = self.timeouts["completion"]
        ddl = time.time() + timeout
        web_port = self.locust_cfg.get("web_port", self.LOCUST_WEB_PORT)

        self.logger.info("\n[runner] === Waiting for completion ===")
        while time.time() < ddl:
            rs = self.client.get()
            if rs is None:
                time.sleep(1)
                continue

            elapsed = self.st_writer.elapsed()
            st = extract_status(rs)
            self.st_writer.write_row(self.phase, st)

            if st.get("rolling_back"):
                if not self.checker.active:
                    self.checker.start(st)
                else:
                    self.checker.check(st, elapsed)

            self._print_line(st, elapsed, web_port)
            if self._completion_met(self.completion, st):
                self.logger.info("\n[runner] Completed at %.2fs", elapsed)
                self.phase = "complete"
                self.st_writer.write_row("complete", st)
                self.checker.stop()
                self._print_line(st, elapsed, web_port, finalized=True)
                return

            time.sleep(1)

        raise TimeoutError(f"Completion timed out after {timeout:.2f}s")

    def _check_rayservice_spec(self) -> None:
        """Check if the RayService spec meets the desired spec after completion.

        This final check passes only if all the following conditions are met:
        1. ray_actor_options.num_cpus in the serve config matches the desired CPU
        2. workerGroupSpecs[].template.spec.containers[].resources.requests.cpu matches the desired CPU
        3. workerGroupSpecs[].template.spec.containers[].resources.limits.cpu matches the desired CPU

        TODO(jwj): Need to consider any other applications fields?
        """
        self.logger.info("[runner] Checking RayService spec after completion...")
        desired_cpu = float(self.completion["worker_cpu"])
        if desired_cpu is None:
            raise ValueError("You must specify the desired CPU in the completion section.")

        rs = self.client.get()
        if rs is None:
            raise RuntimeError("RayService not found after completion")

        for wg in rs["spec"]["rayClusterConfig"]["workerGroupSpecs"]:
            for container in wg["template"]["spec"]["containers"]:
                if container["name"] == "ray-worker":
                    for rsc_key in ["requests", "limits"]:
                        cur_cpu = float(container["resources"][rsc_key]["cpu"])
                        if cur_cpu != desired_cpu:
                            raise RuntimeError(
                                f"Worker {rsc_key}.cpu does not match the desired CPU: "
                                f"current {cur_cpu}, desired {desired_cpu}"
                            )

        rs_spec = rs["spec"]
        self.logger.info("[runner] RayService spec: %s", rs_spec)
        sc = rs_spec.get("serveConfigV2")
        data = yaml.safe_load(sc)
        for app in data.get("applications", []):
            for deploy in app.get("deployments", []):
                opts = deploy.get("ray_actor_options", {})
                cur_cpu = float(opts.get("num_cpus"))
                if cur_cpu != desired_cpu:
                    raise RuntimeError(
                        f"Serve config does not match the desired CPU: "
                        f"current {cur_cpu}, desired {desired_cpu}"
                    )

    @staticmethod
    def _condition_met(condition: dict, st: dict) -> bool:
        if len(condition) == 0:
            raise ValueError("Must specify at least one condition")
        
        for key, val in condition.items():
            if key == "pending_tc_gte":
                v = st.get("pending_tc")
                if v is None or v < val:
                    return False
            elif key == "active_tc_gte":
                v = st.get("active_tc")
                if v is None or v < val:
                    return False
            elif key == "pending_trp_gte":
                v = st.get("pending_trp")
                if v is None or v < val:
                    return False
            elif key == "active_trp_gte":
                v = st.get("active_trp")
                if v is None or v < val:
                    return False
            else:
                # TODO(jwj): Support more condition keys.
                raise ValueError(f"Unknown condition key: {key}")

        return True

    @staticmethod
    def _completion_met(completion: dict, st: dict) -> bool:
        if not (
            # Must meet the following conditions.
            not st.get("upgrading")
            and not st.get("rolling_back")
            # TODO(jwj): Not sure if empty string is sufficient, might need to make sure CR object is deleted.
            and st.get("pending_cluster") == ""
        ):
            return False

        # TODO(jwj): Support more completion keys.
        if "active_trp" in completion and st.get("active_trp") != completion["active_trp"]:
            return False

        return True

    def _print_line(self, st: dict, elapsed: float, web_port: int, finalized: bool = False) -> None:
        """Print status info periodically.

        Note that the finalized line is printed regardless of the PRINT_INTERVAL.
        finalized is True when:
        1. An action condition is met
        2. The load test is completed
        """
        if elapsed - self._last_print < self.PRINT_INTERVAL and not finalized:
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

        rps = get_locust_rps(web_port, self.logger)
        rps_s = f"{rps:.0f}" if rps else "?"

        line = (
            f" [{elapsed:>6.2f}s] {self.phase:<12} | "
            f"Active TC={str(a_tc):>3} TRP={str(a_trp):>3} | "
            f"Pending TC={str(p_tc):>3} TRP={str(p_trp):>3} | "
            f"RPS={rps_s:>4} | {' '.join(flags)}"
        )
        self.logger.info("%s", line)

    def _summary(self):
        duration = time.time() - self.st_writer.start_time
        passed = len(self.checker.violations) == 0
        label = "PASS" if passed else "FAIL"
        self.logger.info("\n%s", "=" * 65)
        self.logger.info("  SCENARIO : %s", self.scenario["name"])
        self.logger.info("  RESULT   : %s", label)
        self.logger.info("  DURATION : %.2fs", duration)
        self.logger.info("  RESULTS  : %s/", self.output_dir)
        if len(self.checker.violations) > 0:
            self.logger.critical("\n BEHAVIOR VIOLATIONS (%s):", len(self.checker.violations))
            for v in self.checker.violations:
                self.logger.critical("    - %s", v)
        else:
            self.logger.info("\n  All monotonicity invariants passed.")
        self.logger.info("%s", "=" * 65)

    def _cleanup(self):
        self.st_writer.close()
        if self.locust_proc is not None and self.locust_proc.poll() is None:
            self.logger.info("[runner] Stopping Locust (SIGINT)...")
            self.locust_proc.send_signal(signal.SIGINT)
            try:
                self.locust_proc.wait(timeout=15)
            except subprocess.TimeoutExpired:
                self.locust_proc.kill()
        if self.port_forward_proc is not None and self.port_forward_proc.poll() is None:
            self.logger.info("[runner] Stopping kubectl port-forward...")
            self.port_forward_proc.send_signal(signal.SIGINT)
            try:
                self.port_forward_proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.port_forward_proc.kill()
        if self.deploy_rayservice:
            self.logger.info("[runner] Deleting RayService...")
            self.client.delete()

        for h in self.logger.handlers[:]:
            self.logger.removeHandler(h)
            h.close()
        logging.shutdown()


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
