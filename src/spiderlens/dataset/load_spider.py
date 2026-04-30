from __future__ import annotations

from pathlib import Path
from typing import Any

from spiderlens.io import read_json


def load_spider_split(spider_dir: Path, split: str = "dev") -> list[dict[str, Any]]:
    path = spider_dir / f"{split}.json"
    if not path.exists():
        raise FileNotFoundError(f"Spider split not found: {path}")
    return read_json(path)


def database_path(spider_dir: Path, db_id: str) -> Path:
    path = spider_dir / "database" / db_id / f"{db_id}.sqlite"
    if not path.exists():
        raise FileNotFoundError(f"SQLite database not found for {db_id}: {path}")
    return path
