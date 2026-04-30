from __future__ import annotations


def label_failure(status: str, error: str = "") -> str:
    if status == "ok":
        return "success"
    lowered = error.lower()
    if "sql" in lowered or "select" in lowered:
        return "sql_error"
    if "json" in lowered or "parse" in lowered:
        return "parse_error"
    if "empty" in lowered:
        return "empty_output"
    return "runtime_error"
