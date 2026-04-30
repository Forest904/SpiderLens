from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class QueryResult:
    columns: list[str]
    rows: list[list[Any]]


class UnsafeSQLStatement(ValueError):
    pass


def execute_select(database: Path, sql: str) -> QueryResult:
    statement = sql.strip().rstrip(";")
    if not statement.lower().startswith(("select", "with")):
        raise UnsafeSQLStatement("Only SELECT/WITH queries are allowed")
    if ";" in statement:
        raise UnsafeSQLStatement("Multiple SQL statements are not allowed")

    uri = f"file:{database.as_posix()}?mode=ro"
    with sqlite3.connect(uri, uri=True) as connection:
        cursor = connection.execute(statement)
        columns = [description[0] for description in cursor.description or []]
        rows = [list(row) for row in cursor.fetchall()]
    return QueryResult(columns=columns, rows=rows)
