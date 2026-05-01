from __future__ import annotations

import re
from pathlib import Path


RUN_ID_PATTERN = re.compile(r"^run_(\d{4})$")


def next_run_id(runs_dir: Path) -> str:
    """Return the next autoincremented run ID for a report/runs directory."""
    highest = 0
    if runs_dir.exists():
        for child in runs_dir.iterdir():
            if not child.is_dir():
                continue
            match = RUN_ID_PATTERN.match(child.name)
            if match:
                highest = max(highest, int(match.group(1)))
    return f"run_{highest + 1:04d}"


def validate_run_id(run_id: str) -> str:
    if not RUN_ID_PATTERN.match(run_id):
        raise ValueError("Run ID must use the format run_0001")
    return run_id
