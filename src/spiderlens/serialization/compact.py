from __future__ import annotations

from typing import Any


def serialize_table(name: str, columns: list[str], rows: list[list[Any]]) -> str:
    lines = [f"{name}({', '.join(columns)})"]
    lines.extend(", ".join(str(cell) for cell in row) for row in rows)
    return "\n".join(lines)
