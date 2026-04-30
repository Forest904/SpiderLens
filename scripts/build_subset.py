from __future__ import annotations

import argparse
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.dataset.load_spider import load_spider_split
    from spiderlens.dataset.subset import write_manifest

    parser = argparse.ArgumentParser(description="Build a manual Spider subset manifest skeleton.")
    parser.add_argument("--spider-dir", type=Path, required=True)
    parser.add_argument("--split", default="dev")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--output", type=Path, default=Path("data/subset/manifest.json"))
    args = parser.parse_args()

    examples = []
    for index, item in enumerate(load_spider_split(args.spider_dir, args.split)[: args.limit], start=1):
        examples.append(
            {
                "example_id": f"{args.split}-{index:04d}",
                "db_id": item["db_id"],
                "question": item["question"],
                "gold_sql": item["query"],
                "oracle_tables": [],
                "rationale": "Add oracle tables and rationale manually.",
            }
        )
    write_manifest(args.output, examples)
    print(f"Wrote {len(examples)} examples to {args.output}")


if __name__ == "__main__":
    main()
