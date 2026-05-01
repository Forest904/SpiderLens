from __future__ import annotations

from pathlib import Path
from typing import Any

from spiderlens.io import read_jsonl, write_json
from spiderlens.reporting.plots import write_metric_plot
from spiderlens.reporting.tables import write_run_markdown_assets


def write_run_report(
    records: list[dict[str, Any]],
    report_runs_dir: Path,
    run_id: str,
    timestamp: str,
    metadata: dict[str, Any],
    baseline_metrics: Path | None = None,
) -> dict[str, Path]:
    run_dir = report_runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    baseline_records = read_jsonl(baseline_metrics) if baseline_metrics else None
    plot_path = write_metric_plot(records, run_dir)
    metadata = {
        **metadata,
        "artifact_links": [
            ("summary", "summary.md"),
            ("per-example metrics", "per_example_metrics.md"),
            ("failure breakdown", "failure_breakdown.md"),
            ("metric deltas", "metric_deltas.md"),
            ("metric plot", "metric_summary.png"),
            ("run journal", "lab_journal.md"),
            ("metadata", "metadata.json"),
        ],
    }
    markdown_paths = write_run_markdown_assets(records, run_dir, timestamp, metadata, baseline_records)
    metadata_path = run_dir / "metadata.json"
    write_json(metadata_path, metadata)
    return {**markdown_paths, "plot": plot_path, "metadata": metadata_path}
