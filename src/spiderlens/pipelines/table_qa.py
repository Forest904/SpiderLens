from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Any

from spiderlens.dataset.load_spider import database_path
from spiderlens.dataset.subset import SubsetExample
from spiderlens.evaluation.normalize import normalize_rows
from spiderlens.llm_client import CachedLLMClient
from spiderlens.parsing.answer_output import parse_answer_rows
from spiderlens.prompts.table_qa import build_table_qa_prompt
from spiderlens.serialization.markdown import serialize_table


def serialize_oracle_tables(database: Path, table_names: list[str]) -> str:
    chunks: list[str] = []
    uri = f"file:{database.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        for table in table_names:
            cursor = connection.execute(f'SELECT * FROM "{table}"')
            columns = [description[0] for description in cursor.description or []]
            rows = [list(row) for row in cursor.fetchall()]
            chunks.append(serialize_table(table, columns, rows))
    return "\n\n".join(chunks)


def run_example(example: SubsetExample, spider_dir: Path, client: CachedLLMClient, refresh: bool = False) -> dict[str, Any]:
    started = time.time()
    try:
        db_path = database_path(spider_dir, example.db_id)
        tables = serialize_oracle_tables(db_path, example.oracle_tables)
        prompt = build_table_qa_prompt(example.question, tables)
        completion = client.complete(prompt, refresh=refresh)
        rows = parse_answer_rows(completion["text"])
        return {
            "example_id": example.example_id,
            "db_id": example.db_id,
            "pipeline": "table_qa",
            "status": "ok",
            "prompt_hash": completion["cache_key"],
            "cached": completion["cached"],
            "raw_response": completion["text"],
            "rows": rows,
            "normalized_rows": normalize_rows(rows),
            "elapsed_seconds": round(time.time() - started, 3),
            "error": "",
        }
    except Exception as exc:
        return {
            "example_id": example.example_id,
            "db_id": example.db_id,
            "pipeline": "table_qa",
            "status": "failed",
            "elapsed_seconds": round(time.time() - started, 3),
            "error": str(exc),
        }
