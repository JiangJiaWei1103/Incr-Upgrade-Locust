#!/usr/bin/env python3
"""
This script is used to generate a markdown report from the load test output.

Usage:
    python report.py --output-dir outputs/rollback/
"""

import argparse
import csv
from pathlib import Path


STATUS_LOG_FILE = "status_log.csv"
LOCUST_STATS_FILE = "locust_stats.csv"


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with open(path) as f:
        return list(csv.DictReader(f))


def parse_locust_stats(locust_rows: list[dict]) -> dict | None:
    """Parse the locust stats for the Aggregated row."""
    for row in locust_rows:
        if row.get("Name") == "Aggregated":
            return {
                "total_requests": int(row.get("Request Count", 0)),
                "total_failures": int(row.get("Failure Count", 0)),
                "avg_response_time": row.get("Average Response Time", "?"),
                "p99_response_time": row.get("99%", "?"),
                "rps": row.get("Requests/s", "?"),
            }

    return None


def get_violations(status_rows: list[dict]) -> list[str]:
    violations = []
    prev = {}
    for row in status_rows:
        if not row.get("rolling_back", "").lower() == "true":
            continue

        if len(prev) == 0:
            prev = {
                "active_tc": _int_or_none(row.get("active_tc")),
                "active_trp": _int_or_none(row.get("active_trp")),
                "pending_tc": _int_or_none(row.get("pending_tc")),
                "pending_trp": _int_or_none(row.get("pending_trp")),
            }
            continue

        checks = [
            ("active_tc", "increasing"),
            ("active_trp", "increasing"),
            ("pending_tc", "decreasing"),
            ("pending_trp", "decreasing"),
        ]
        for field, direction in checks:
            cur = _int_or_none(row.get(field))
            p = prev.get(field)
            if cur is None or p is None:
                # TODO(jwj): Make this more robust.
                continue
            if direction == "increasing" and cur < p:
                violations.append(
                    f"[{row['elapsed_s']}s] {field} decreased: {p} -> {cur}"
                )
            elif direction == "decreasing" and cur > p:
                violations.append(
                    f"[{row['elapsed_s']}s] {field} increased: {p} -> {cur}"
                )
            prev[field] = cur

    return violations


def generate_report(output_dir: str, sample_interval: int = 5) -> str:
    output_dir = Path(output_dir)
    locust_rows = read_csv(output_dir / LOCUST_STATS_FILE)
    status_rows = read_csv(output_dir / STATUS_LOG_FILE)

    locust_summary = parse_locust_stats(locust_rows)
    # TODO(jwj): Might be simpler to parse the log file.
    violations = get_violations(status_rows)
    passed = len(violations) == 0

    scenario_name = output_dir.name
    lines = []
    lines.append(f"## {scenario_name}")
    lines.append("")
    lines.append(f"### Result: {'PASS' if passed else 'FAIL'}")
    lines.append("")
    
    if locust_summary:
        total_req = locust_summary["total_requests"]
        total_fail = locust_summary["total_failures"]
        fail_pct = (
            f"{total_fail / total_req * 100:.2f}%" if total_req > 0 else "N/A"
        )
        lines.append("### Locust Summary")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Total Requests | {total_req:,} |")
        lines.append(f"| Total Failures | {total_fail:,} |")
        lines.append(f"| Failure Rate | {fail_pct} |")
        lines.append(f"| Avg Response Time | {float(locust_summary['avg_response_time']):.4f}ms |")
        lines.append(f"| P99 Response Time | {float(locust_summary['p99_response_time']):.4f}ms |")
        lines.append(f"| RPS | {float(locust_summary['rps']):.2f}reqs/s |")
        lines.append("")

    lines.append("### Test Goals")
    lines.append("")
    inv_labels = [
        ("active_tc monotonically increasing during rollback", "active_tc"),
        ("active_trp monotonically increasing during rollback", "active_trp"),
        ("pending_tc monotonically decreasing during rollback", "pending_tc"),
        ("pending_trp monotonically decreasing during rollback", "pending_trp"),
    ]
    for label, field in inv_labels:
        has_violation = any(field in v for v in violations)
        mark = "x" if not has_violation else " "
        lines.append(f"- [{mark}] {label}")

    if locust_summary:
        zero_fail = locust_summary["total_failures"] == 0
        mark = "x" if zero_fail else " "
        lines.append(f"- [{mark}] Zero Locust failures")
    lines.append("")

    if len(violations) > 0:
        lines.append("### Monotonicity Violations")
        lines.append("")
        for v in violations:
            lines.append(f"- {v}")
        lines.append("")

    lines.append("### Timeline")
    lines.append("")
    lines.append(
        "| Elapsed | Phase | Active TC | Active TRP | "
        "Pending TC | Pending TRP | Upgrading | Rolling Back |"
    )
    lines.append("|---------|-------|-----------|------------|------------|-------------|-----------|--------------|")

    # Preserve the entire timeline for debugging purposes.
    # last_sampled = -sample_interval
    # prev_phase = None
    for row in status_rows:
        elapsed = float(row.get("elapsed_s", 0))
        phase = row.get("phase", "")

        # Always include phase transitions and first/last rows
        # phase_changed = phase != prev_phase
        # should_sample = (elapsed - last_sampled) >= sample_interval

        # if should_sample or phase_changed:
        if True:
            a_tc = row.get("active_tc", "")
            a_trp = row.get("active_trp", "")
            p_tc = row.get("pending_tc", "") or "-"
            p_trp = row.get("pending_trp", "") or "-"
            upg = row.get("upgrading", "")
            rb = row.get("rolling_back", "")
            lines.append(
                f"| {elapsed:>7.1f} | {phase:<12} | {str(a_tc):>9} | "
                f"{str(a_trp):>10} | {str(p_tc):>10} | "
                f"{str(p_trp):>11} | {str(upg):>9} | {str(rb):>12} |"
            )
            # last_sampled = elapsed
            # prev_phase = phase

    # if state_rows:
    #     row = state_rows[-1]
    #     elapsed = float(row.get("elapsed_s", 0))
    #     if elapsed > last_sampled:
    #         a_tc = row.get("active_tc", "")
    #         a_trp = row.get("active_trp", "")
    #         p_tc = row.get("pending_tc", "") or "-"
    #         p_trp = row.get("pending_trp", "") or "-"
    #         upg = row.get("upgrading", "")
    #         rb = row.get("rolling_back", "")
    #         lines.append(
    #             f"| {elapsed:>7.1f} | {row.get('phase',''):<12} | {str(a_tc):>9} | "
    #             f"{str(a_trp):>10} | {str(p_tc):>10} | "
    #             f"{str(p_trp):>11} | {str(upg):>9} | {str(rb):>12} |"
    #         )

    lines.append("")
    return "\n".join(lines)


def _int_or_none(val: str) -> int | None:
    if val is None or val == "" or val == "None":
        return None
    try:
        return int(float(val))
    except Exception as e:
        raise ValueError(f"Error converting {val} to int: {e}")


def main():
    parser = argparse.ArgumentParser(description="Generate load test report")
    parser.add_argument(
        "--output-dir", required=True,
        help="Path to output directory (e.g., outputs/rollback/)",
    )
    parser.add_argument(
        "--sample-interval", type=int, default=5,
        help="Sample interval in seconds for the timeline table (default: 5)",
    )
    args = parser.parse_args()

    report = generate_report(args.output_dir, args.sample_interval)
    out_path = Path(args.output_dir) / "report.md"
    with open(out_path, "w") as f:
        f.write(report)


if __name__ == "__main__":
    main()
