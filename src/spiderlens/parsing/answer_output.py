from __future__ import annotations

import json
import re
from typing import Any


FENCED_BLOCK = re.compile(r"```(?:json)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def parse_answer_rows(text: str) -> list[list[Any]]:
    match = FENCED_BLOCK.search(text)
    candidate = (match.group(1) if match else text).strip()
    data = json.loads(candidate)
    if not isinstance(data, list):
        raise ValueError("Answer must be a JSON list")
    rows: list[list[Any]] = []
    for item in data:
        rows.append(item if isinstance(item, list) else [item])
    return rows
