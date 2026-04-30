from __future__ import annotations

import json
from typing import Any


def serialize_table(name: str, columns: list[str], rows: list[list[Any]]) -> str:
    records = [dict(zip(columns, row, strict=False)) for row in rows]
    return json.dumps({name: records}, ensure_ascii=False, indent=2)
