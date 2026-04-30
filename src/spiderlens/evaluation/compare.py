from __future__ import annotations

from pathlib import Path
from typing import Any

from spiderlens.dataset.load_spider import database_path
from spiderlens.dataset.subset import SubsetExample
from spiderlens.evaluation.metrics import compute_metrics
from spiderlens.evaluation.normalize import normalize_rows
from spiderlens.execution.sqlite_runner import execute_select


def evaluate_record(record: dict[str, Any], example: SubsetExample, spider_dir: Path) -> dict[str, Any]:
    expected_result = execute_select(database_path(spider_dir, example.db_id), example.gold_sql)
    expected = normalize_rows(expected_result.rows)
    predicted = normalize_rows(record.get("rows", [])) if record.get("status") == "ok" else []
    metrics = compute_metrics(predicted, expected)
    return {
        "example_id": example.example_id,
        "db_id": example.db_id,
        "pipeline": record.get("pipeline", "unknown"),
        "status": record.get("status", "unknown"),
        **metrics,
        "error": record.get("error", ""),
    }
