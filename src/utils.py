"""Utility functions."""
import csv
import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path

import yaml


class RayServiceClient:
    """A thin kubectl wrapper for RayService CRUD operations."""

    def __init__(
        self,
        namespace: str = "default",
        name: str = "simple-locust",
        *,
        logger: logging.Logger | None = None,
    ) -> None:
        self.namespace = namespace
        self.name = name
        self.logger = logger

    def get(self) -> dict | None:
        result = subprocess.run(
            ["kubectl", "get", "rayservice", self.name,
             "-n", self.namespace, "-o", "json"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)

    def apply(self, yaml_path: str) -> None:
        result = subprocess.run(
            ["kubectl", "apply", "-f", yaml_path, "-n", self.namespace],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(f"kubectl apply failed: {result.stderr}")

    def put(self, cpu: str, max_retries: int = 5) -> None:
        for attempt in range(max_retries):
            rs = self.get()
            if rs is None:
                self.logger.info(
                    "[rayservice_client] RayService not found, retrying... (%s/%s)",
                    attempt + 1,
                    max_retries,
                )
                time.sleep(0.5)
                continue

            for wg in rs["spec"]["rayClusterConfig"]["workerGroupSpecs"]:
                for container in wg["template"]["spec"]["containers"]:
                    if container["name"] == "ray-worker":
                        container["resources"]["requests"]["cpu"] = cpu
                        container["resources"]["limits"]["cpu"] = cpu

            sc = rs["spec"].get("serveConfigV2")
            if sc is not None:
                rs["spec"]["serveConfigV2"] = _sync_serve_config_v2_cpu(sc, cpu)

            # TODO(jwj): Don't use imperative command?
            result = subprocess.run(
                ["kubectl", "replace", "-f", "-"],
                input=json.dumps(rs), capture_output=True, text=True,
            )
            if result.returncode == 0:
                return

            # if "the object has been modified" in result.stderr and attempt < max_retries - 1:
            if len(result.stderr) > 0 and attempt < max_retries - 1:
                time.sleep(0.5)
                continue
            raise RuntimeError(f"kubectl replace failed after {attempt + 1} attempts: {result.stderr}")

    def delete(self) -> None:
        subprocess.run(
            ["kubectl", "delete", "rayservice", self.name,
             "-n", self.namespace, "--ignore-not-found"],
            capture_output=True, text=True,
        )

    # def get_gateway_ip(self) -> str | None:
    #     """Unused now."""
    #     gw_name = f"{self.name}-gateway"
    #     result = subprocess.run(
    #         ["kubectl", "get", "gateway", gw_name, "-n", self.namespace,
    #          "-o", "jsonpath={.status.addresses[0].value}"],
    #         capture_output=True, text=True,
    #     )
    #     if result.returncode == 0 and result.stdout.strip():
    #         return result.stdout.strip()
    #     return None

    def port_forward_gateway(self, local_port: int = 8080, remote_port: int = 80) -> subprocess.Popen:
        """Port forward the Gateway service as the locust entry point."""
        svc_name = f"{self.name}-gateway-istio"
        cmd = [
            "kubectl",
            "port-forward",
            f"svc/{svc_name}",
            f"{local_port}:{remote_port}",
            "-n",
            self.namespace,
        ]
        return subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def _sync_serve_config_v2_cpu(serve_config_v2: str, cpu: str) -> str:
    """Set each deployment's ray_actor_options.num_cpus to match worker CPU."""
    if len(str(serve_config_v2).strip()) == 0:
        return serve_config_v2

    data = yaml.safe_load(serve_config_v2)
    if data is None or not isinstance(data, dict):
        return serve_config_v2

    n = _k8s_cpu_to_num_cpus(cpu)
    for app in data.get("applications") or []:
        if not isinstance(app, dict):
            continue
        for deploy in app.get("deployments") or []:
            if not isinstance(deploy, dict):
                continue
            opts = deploy.get("ray_actor_options")
            if not isinstance(opts, dict):
                continue
            _ = opts.pop("num-cpus", None)
            opts["num_cpus"] = n
    return yaml.safe_dump(data, default_flow_style=False, sort_keys=False)


def _k8s_cpu_to_num_cpus(cpu: str) -> float:
    """Map a Kubernetes CPU quantity (e.g. 500m, 2) to a Ray num_cpus value."""
    s = cpu.strip()
    if s.endswith("m"):
        v = float(s[:-1]) / 1000.0
    else:
        v = float(s)
    # if v == int(v):
    #     return int(v)

    return v


def extract_status(rs_json: dict) -> dict:
    """Extract RayService status fields."""
    if len(rs_json) == 0:
        raise ValueError("RayService JSON is empty")

    status = rs_json.get("status", {})
    active = status.get("activeServiceStatus", {})
    pending = status.get("pendingServiceStatus", {})
    conditions = {c["type"]: c for c in status.get("conditions", [])}

    # RayService is "ready" when active cluster exists and all apps are RUNNING.
    # TODO(jwj): Make sure this is safe. Note that head Pod readiness doesn't guarantee RayService can serve traffic.
    app_statuses = active.get("applicationStatuses", {})
    ready = (
        bool(active.get("rayClusterName"))
        and bool(app_statuses)
        and all(s.get("status") == "RUNNING" for s in app_statuses.values())
    )

    return {
        "active_cluster": active.get("rayClusterName", ""),
        "active_tc": active.get("targetCapacity"),
        "active_trp": active.get("trafficRoutedPercent"),
        "pending_cluster": pending.get("rayClusterName", ""),
        "pending_tc": pending.get("targetCapacity"),
        "pending_trp": pending.get("trafficRoutedPercent"),
        "upgrading": conditions.get("UpgradeInProgress", {}).get("status") == "True",
        "rolling_back": conditions.get("RollbackInProgress", {}).get("status") == "True",
        "ready": ready,
    }


class StatusWriter:
    """Snapshots the RayService status and the load test status."""

    CSV_FIELDS = [
        "timestamp", "elapsed_s", "phase",
        "active_cluster", "active_tc", "active_trp",
        "pending_cluster", "pending_tc", "pending_trp",
        "upgrading", "rolling_back",
    ]

    def __init__(self, output_path: Path) -> None:
        self.start_time = time.time()
        self.rows = []
        self._file = open(output_path, "w", newline="")
        self._writer = csv.DictWriter(self._file, fieldnames=self.CSV_FIELDS)
        self._writer.writeheader()

    def write_row(self, phase: str, status: dict) -> None:
        row = {
            "timestamp": datetime.now().isoformat(),
            "elapsed_s": round(time.time() - self.start_time, 2),
            "phase": phase,
            "active_cluster": status.get("active_cluster", ""),
            "active_tc": status.get("active_tc"),
            "active_trp": status.get("active_trp"),
            "pending_cluster": status.get("pending_cluster", ""),
            "pending_tc": status.get("pending_tc"),
            "pending_trp": status.get("pending_trp"),
            "upgrading": status.get("upgrading", False),
            "rolling_back": status.get("rolling_back", False),
        }
        self._writer.writerow(row)
        self._file.flush()
        self.rows.append(row)

    def elapsed(self) -> float:
        return time.time() - self.start_time

    def close(self) -> None:
        self._file.close()


class StatusChecker:
    """Validates monotonicity during rollback.
    
    TODO(jwj): Enrich behavioral checks.
    """

    def __init__(self) -> None:
        self.active = False
        self.prev = {}
        self.violations = []

    def start(self, status: dict) -> None:
        """Snapshot current values as the baseline for monotonicity checks."""
        self.active = True
        self.prev = {
            "active_tc": status.get("active_tc"),
            "active_trp": status.get("active_trp"),
            "pending_tc": status.get("pending_tc"),
            "pending_trp": status.get("pending_trp"),
        }

    def check(self, status: dict, elapsed_s: float) -> None:
        if not self.active:
            return

        checks = [
            ("active_tc", "increasing"),
            ("active_trp", "increasing"),
            ("pending_tc", "decreasing"),
            ("pending_trp", "decreasing"),
        ]
        for field, direction in checks:
            cur = status.get(field)
            prev = self.prev.get(field)
            if cur is None or prev is None:
                self.violations.append(
                    f"[{elapsed_s}s] {field} missing: {prev} -> {cur}"
                )
                continue

            if direction == "increasing" and cur < prev:
                self.violations.append(
                    f"[{elapsed_s}s] {field} decreased: {prev} -> {cur}"
                )
            elif direction == "decreasing" and cur > prev:
                self.violations.append(
                    f"[{elapsed_s}s] {field} increased: {prev} -> {cur}"
                )

            self.prev[field] = cur


def get_locust_rps(
    web_port: int,
    logger: logging.Logger | None = None,
) -> float | None:
    """Best-effort RPS query via Locust REST API."""
    try:
        import requests
        resp = requests.get(f"http://localhost:{web_port}/stats/requests", timeout=2)
        if resp.status_code == 200:
            for stat in resp.json().get("stats", []):
                if stat.get("name") == "Aggregated":
                    return stat.get("current_rps", 0.0)
    except Exception as e:
        logger.warning("[get_locust_rps] Error getting Locust RPS: %s", e)

    return None


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    _FMT = "%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) | %(message)s"
    FORMATS = {
        logging.DEBUG: grey + _FMT + reset,
        logging.INFO: cyan + _FMT + reset,
        logging.WARNING: yellow + _FMT + reset,
        logging.ERROR: red + _FMT + reset,
        logging.CRITICAL: bold_red + _FMT + reset
    }

    def format(self, record: logging.LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")

        return formatter.format(record)