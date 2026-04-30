from __future__ import annotations

import re


FENCED_BLOCK = re.compile(r"```(?:sql)?\s*(.*?)```", re.IGNORECASE | re.DOTALL)


def extract_sql(text: str) -> str:
    match = FENCED_BLOCK.search(text)
    candidate = match.group(1) if match else text
    candidate = candidate.strip()
    if not candidate:
        raise ValueError("No SQL found in model output")
    return candidate.rstrip(";") + ";"
