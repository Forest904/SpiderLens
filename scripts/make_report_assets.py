from __future__ import annotations

import argparse
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.io import read_jsonl
    from spiderlens.reporting.run_report import write_run_report
    from spiderlens.reporting.runs import next_run_id, validate_run_id

    parser = argparse.ArgumentParser(description="Generate run-scoped Markdown tables and figures from metric JSONL.")
    parser.add_argument("--metrics", type=Path, default=Path("data/outputs/metrics.jsonl"))
    parser.add_argument("--runs-dir", type=Path, default=Path("report/runs"))
    parser.add_argument("--run-id", default="")
    parser.add_argument("--timestamp", default="")
    parser.add_argument("--baseline-metrics", type=Path)
    args = parser.parse_args()

    from datetime import datetime

    run_id = validate_run_id(args.run_id) if args.run_id else next_run_id(args.runs_dir)
    timestamp = args.timestamp or datetime.now().strftime("%Y-%m-%d_%H%M%S")
    records = read_jsonl(args.metrics)
    metadata = {
        "run_id": run_id,
        "timestamp": timestamp,
        "date": timestamp.split("_")[0],
        "manifest_path": "unknown",
        "model": "unknown",
        "base_url": "unknown",
        "temperature": "unknown",
        "prompt_strategy": "unknown",
        "serialization_strategy": "unknown",
        "record_counts": {"metrics": len(records)},
        "commands": [f".\\.venv\\Scripts\\python.exe scripts\\make_report_assets.py --metrics {args.metrics} --run-id {run_id}"],
    }
    paths = write_run_report(records, args.runs_dir, run_id, timestamp, metadata, args.baseline_metrics)
    print("Wrote report assets:")
    for name, path in paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
