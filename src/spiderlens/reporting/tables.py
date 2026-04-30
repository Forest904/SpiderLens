from __future__ import annotations

from pathlib import Path


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

    metric_cols = ["cell_precision", "cell_recall", "tuple_cardinality"]
    per_example_cols = ["pipeline", "example_id", "db_id", "status", *metric_cols, "error"]
    paths["per_example"].write_text(markdown_table(records, per_example_cols), encoding="utf-8")

    grouped: dict[str, list[dict]] = {}
    for record in records:
        grouped.setdefault(str(record.get("pipeline", "unknown")), []).append(record)
    summary_records = []
    for pipeline, items in sorted(grouped.items()):
        row = {"pipeline": pipeline}
        for metric in metric_cols:
            values = [float(item.get(metric, 0.0)) for item in items]
            row[metric] = round(sum(values) / len(values), 4)
        summary_records.append(row)
    paths["summary"].write_text(markdown_table(summary_records, ["pipeline", *metric_cols]), encoding="utf-8")

    counts: dict[tuple[str, str], int] = {}
    for record in records:
        key = (str(record.get("pipeline", "unknown")), str(record.get("status", "unknown")))
        counts[key] = counts.get(key, 0) + 1
    failure_records = [{"pipeline": key[0], "status": key[1], "count": count} for key, count in sorted(counts.items())]
    paths["failures"].write_text(markdown_table(failure_records, ["pipeline", "status", "count"]), encoding="utf-8")
    return paths


def markdown_table(records: list[dict], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for record in records:
        values = [str(record.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines) + "\n"
