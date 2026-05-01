from __future__ import annotations

from pathlib import Path
from typing import Any


METRIC_COLS = ["cell_precision", "cell_recall", "tuple_cardinality"]


def write_summary_tables(records: list[dict], output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "per_example": output_dir / "per_example_metrics.md",
        "summary": output_dir / "summary_metrics.md",
        "failures": output_dir / "failure_breakdown.md",
    }
    if not records:
        for path in paths.values():
            path.write_text("_No records available._\n", encoding="utf-8")
        return paths

    per_example_cols = ["pipeline", "example_id", "db_id", "status", *METRIC_COLS, "error"]
    paths["per_example"].write_text(markdown_table(records, per_example_cols), encoding="utf-8")

    summary_records = aggregate_metric_means(records)
    paths["summary"].write_text(markdown_table(summary_records, ["pipeline", *METRIC_COLS]), encoding="utf-8")

    failure_records = failure_breakdown(records)
    paths["failures"].write_text(
        markdown_table(failure_records, ["pipeline", "failure_label", "db_id", "query_pattern", "count"]),
        encoding="utf-8",
    )
    return paths


def write_run_markdown_assets(
    records: list[dict[str, Any]],
    run_dir: Path,
    timestamp: str,
    metadata: dict[str, Any],
    baseline_records: list[dict[str, Any]] | None = None,
) -> dict[str, Path]:
    run_dir.mkdir(parents=True, exist_ok=True)

    per_example_text = markdown_table(
        records,
        [
            "run_id",
            "pipeline",
            "example_id",
            "db_id",
            "query_pattern",
            "status",
            "failure_label",
            *METRIC_COLS,
            "error",
        ],
    )
    failure_text = markdown_table(
        failure_breakdown(records),
        ["pipeline", "failure_label", "db_id", "query_pattern", "count"],
    )
    delta_text = metric_delta_markdown(records, baseline_records)
    summary_text = run_summary_markdown(metadata, records, failure_text, delta_text)
    journal_text = run_journal_markdown(metadata, records)

    files = {
        "summary": "summary.md",
        "per_example": "per_example_metrics.md",
        "failures": "failure_breakdown.md",
        "deltas": "metric_deltas.md",
        "journal": "lab_journal.md",
    }
    timestamped_files = {
        "summary_timestamped": f"{timestamp}_summary.md",
        "per_example_timestamped": f"{timestamp}_per_example_metrics.md",
        "failures_timestamped": f"{timestamp}_failure_breakdown.md",
        "deltas_timestamped": f"{timestamp}_metric_deltas.md",
        "journal_timestamped": f"{timestamp}_lab_journal.md",
    }
    contents = {
        "summary": summary_text,
        "per_example": per_example_text,
        "failures": failure_text,
        "deltas": delta_text,
        "journal": journal_text,
    }

    paths: dict[str, Path] = {}
    for key, filename in files.items():
        path = run_dir / filename
        path.write_text(contents[key], encoding="utf-8")
        paths[key] = path
    for key, filename in timestamped_files.items():
        content_key = key.replace("_timestamped", "")
        if content_key == "failures":
            content_key = "failures"
        path = run_dir / filename
        path.write_text(contents[content_key], encoding="utf-8")
        paths[key] = path
    return paths


def aggregate_metric_means(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for record in records:
        grouped.setdefault(str(record.get("pipeline", "unknown")), []).append(record)

    summary_records = []
    for pipeline, items in sorted(grouped.items()):
        row: dict[str, Any] = {"pipeline": pipeline, "records": len(items)}
        for metric in METRIC_COLS:
            values = [float(item.get(metric, 0.0)) for item in items]
            row[metric] = round(sum(values) / len(values), 4)
        summary_records.append(row)
    return summary_records


def failure_breakdown(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    counts: dict[tuple[str, str, str, str], int] = {}
    for record in records:
        key = (
            str(record.get("pipeline", "unknown")),
            str(record.get("failure_label", record.get("status", "unknown"))),
            str(record.get("db_id", "unknown")),
            str(record.get("query_pattern", "unknown")),
        )
        counts[key] = counts.get(key, 0) + 1
    return [
        {
            "pipeline": key[0],
            "failure_label": key[1],
            "db_id": key[2],
            "query_pattern": key[3],
            "count": count,
        }
        for key, count in sorted(counts.items())
    ]


def metric_delta_markdown(
    current_records: list[dict[str, Any]],
    baseline_records: list[dict[str, Any]] | None,
) -> str:
    if baseline_records is None:
        return "_No baseline metrics path was provided._\n"
    baseline_by_pipeline = {row["pipeline"]: row for row in aggregate_metric_means(baseline_records)}
    rows = []
    for current in aggregate_metric_means(current_records):
        pipeline = current["pipeline"]
        baseline = baseline_by_pipeline.get(pipeline, {})
        row: dict[str, Any] = {"pipeline": pipeline}
        for metric in METRIC_COLS:
            current_value = float(current.get(metric, 0.0))
            baseline_value = float(baseline.get(metric, 0.0))
            row[f"{metric}_current"] = round(current_value, 4)
            row[f"{metric}_baseline"] = round(baseline_value, 4)
            row[f"{metric}_delta"] = round(current_value - baseline_value, 4)
        rows.append(row)
    columns = ["pipeline"]
    for metric in METRIC_COLS:
        columns.extend([f"{metric}_current", f"{metric}_baseline", f"{metric}_delta"])
    return markdown_table(rows, columns)


def run_summary_markdown(
    metadata: dict[str, Any],
    records: list[dict[str, Any]],
    failure_text: str,
    delta_text: str,
) -> str:
    aggregate_text = markdown_table(aggregate_metric_means(records), ["pipeline", "records", *METRIC_COLS])
    counts = metadata.get("record_counts", {})
    commands = metadata.get("commands", [])
    artifact_links = metadata.get("artifact_links", [])
    lines = [
        f"# Run Summary: {metadata.get('run_id', '')}",
        "",
        f"- Timestamp: `{metadata.get('timestamp', '')}`",
        f"- Manifest: `{metadata.get('manifest_path', '')}`",
        f"- Model: `{metadata.get('model', '')}`",
        f"- Base URL: `{metadata.get('base_url', '')}`",
        f"- Temperature: `{metadata.get('temperature', '')}`",
        f"- Prompt strategy: `{metadata.get('prompt_strategy', '')}`",
        f"- Serialization strategy: `{metadata.get('serialization_strategy', '')}`",
        f"- Text-to-SQL records: `{counts.get('text_to_sql', 0)}`",
        f"- Table QA records: `{counts.get('table_qa', 0)}`",
        f"- Metric records: `{counts.get('metrics', len(records))}`",
        "",
        "## Reproduction Commands",
        "",
        "```powershell",
        *commands,
        "```",
        "",
        "## Aggregate Metrics",
        "",
        aggregate_text.rstrip(),
        "",
        "## Failure Counts",
        "",
        failure_text.rstrip(),
        "",
        "## Metric Deltas",
        "",
        delta_text.rstrip(),
        "",
        "## Artifacts",
        "",
    ]
    lines.extend(f"- [{name}]({path})" for name, path in artifact_links)
    return "\n".join(lines) + "\n"


def run_journal_markdown(metadata: dict[str, Any], records: list[dict[str, Any]]) -> str:
    failures = [record for record in records if record.get("failure_label") != "success"]
    return "\n".join(
        [
            f"# Lab Journal: {metadata.get('run_id', '')}",
            "",
            f"Date: {metadata.get('date', '')}",
            "Goal: Strengthen the reporting pipeline with reproducible run-scoped artifacts.",
            "Run ID / command:",
            "",
            "```powershell",
            *metadata.get("commands", []),
            "```",
            "",
            "Generated metrics:",
            "",
            markdown_table(aggregate_metric_means(records), ["pipeline", "records", *METRIC_COLS]).rstrip(),
            "",
            "Report artifacts:",
            "",
            *[f"- [{name}]({path})" for name, path in metadata.get("artifact_links", [])],
            "",
            "Failures or surprises:",
            f"- Failed metric records: {len(failures)}",
            "",
            "Interpretation:",
            "- This run preserves metadata, metrics, failures, deltas, and report links in one run folder.",
            "",
            "Next action:",
            "- Use these run folders as the baseline trace before prompt and parser iteration.",
            "",
        ]
    )


def markdown_table(records: list[dict], columns: list[str]) -> str:
    if not records:
        return "_No records available._\n"
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for record in records:
        values = [str(record.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"
