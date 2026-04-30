from __future__ import annotations

import time
from pathlib import Path
from typing import Any

from spiderlens.dataset.load_spider import database_path
from spiderlens.dataset.schema import extract_schema
from spiderlens.dataset.subset import SubsetExample
from spiderlens.evaluation.normalize import normalize_rows
from spiderlens.execution.sqlite_runner import execute_select
from spiderlens.llm_client import CachedLLMClient
from spiderlens.parsing.sql_output import extract_sql
from spiderlens.prompts.text_to_sql import build_text_to_sql_prompt


def run_example(example: SubsetExample, spider_dir: Path, client: CachedLLMClient, refresh: bool = False) -> dict[str, Any]:
    started = time.time()
    try:
        db_path = database_path(spider_dir, example.db_id)
        schema = extract_schema(db_path, example.oracle_tables)
        prompt = build_text_to_sql_prompt(example.question, schema, example.oracle_tables)
        completion = client.complete(prompt, refresh=refresh)
        sql = extract_sql(completion["text"])
        result = execute_select(db_path, sql)
        return {
            "example_id": example.example_id,
            "db_id": example.db_id,
            "pipeline": "text_to_sql",
            "status": "ok",
            "prompt_hash": completion["cache_key"],
            "cached": completion["cached"],
            "raw_response": completion["text"],
            "sql": sql,
            "columns": result.columns,
            "rows": result.rows,
            "normalized_rows": normalize_rows(result.rows),
            "elapsed_seconds": round(time.time() - started, 3),
            "error": "",
        }
    except Exception as exc:
        return {
            "example_id": example.example_id,
            "db_id": example.db_id,
            "pipeline": "text_to_sql",
            "status": "failed",
            "elapsed_seconds": round(time.time() - started, 3),
            "error": str(exc),
        }
