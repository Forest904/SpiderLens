from __future__ import annotations

import sqlite3
from pathlib import Path


def extract_schema(database: Path, tables: list[str] | None = None) -> str:
    selected = set(tables or [])
    with sqlite3.connect(database) as connection:
        table_rows = connection.execute(
            "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        ).fetchall()

    lines: list[str] = []
    for name, create_sql in table_rows:
        if selected and name not in selected:
            continue
        lines.append(f"-- {name}")
        lines.append(create_sql or f"TABLE {name}")
    return "\n".join(lines)
