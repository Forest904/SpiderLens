from __future__ import annotations

from typing import Any


def normalize_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value).strip().lower()


def normalize_rows(rows: list[list[Any]], sort_rows: bool = True) -> list[tuple[str, ...]]:
    normalized = [tuple(normalize_cell(cell) for cell in row) for row in rows]
    return sorted(normalized) if sort_rows else normalized


def cells(rows: list[tuple[str, ...]]) -> list[str]:
    return [cell for row in rows for cell in row]
