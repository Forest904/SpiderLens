from __future__ import annotations

from typing import Any


def serialize_table(name: str, columns: list[str], rows: list[list[Any]]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
    return "\n".join([f"### {name}", header, separator, *body])
