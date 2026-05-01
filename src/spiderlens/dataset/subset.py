from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from spiderlens.io import read_json, write_json


@dataclass(frozen=True)
class SubsetExample:
    example_id: str
    db_id: str
    question: str
    gold_sql: str
    oracle_tables: list[str]
    rationale: str = ""
    query_pattern: str = "unknown"


def load_manifest(path: Path) -> list[SubsetExample]:
    data = read_json(path)
    examples = data["examples"] if isinstance(data, dict) else data
    return [
        SubsetExample(
            example_id=item["example_id"],
            db_id=item["db_id"],
            question=item["question"],
            gold_sql=item["gold_sql"],
            oracle_tables=list(item.get("oracle_tables", [])),
            rationale=item.get("rationale", ""),
            query_pattern=item.get("query_pattern", "unknown"),
        )
        for item in examples
    ]


def write_manifest(path: Path, examples: list[dict[str, Any]]) -> None:
    write_json(path, {"examples": examples})
