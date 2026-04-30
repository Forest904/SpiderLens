from __future__ import annotations

import argparse
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.config import load_settings
    from spiderlens.dataset.subset import load_manifest
    from spiderlens.io import write_jsonl
    from spiderlens.llm_client import CachedLLMClient, LLMConfig
    from spiderlens.pipelines.table_qa import run_example

    parser = argparse.ArgumentParser(description="Run the Direct Table QA pipeline.")
    parser.add_argument("--manifest", type=Path, default=Path("data/subset/manifest.json"))
    parser.add_argument("--output", type=Path, default=Path("data/outputs/table_qa.jsonl"))
    parser.add_argument("--refresh-cache", action="store_true")
    args = parser.parse_args()

    settings = load_settings()
    client = CachedLLMClient(
        LLMConfig(settings.llm_api_key, settings.llm_base_url, settings.llm_model, settings.temperature),
        settings.spiderlens_output_dir / "cache",
    )
    records = [run_example(example, settings.spider_data_dir, client, args.refresh_cache) for example in load_manifest(args.manifest)]
    write_jsonl(args.output, records)
    print(f"Wrote {len(records)} records to {args.output}")


if __name__ == "__main__":
    main()
