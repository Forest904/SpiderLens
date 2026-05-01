from __future__ import annotations

import argparse
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.config import load_settings
    from spiderlens.dataset.subset import load_manifest
    from spiderlens.evaluation.compare import evaluate_record
    from spiderlens.io import read_jsonl, write_jsonl

    parser = argparse.ArgumentParser(description="Evaluate pipeline outputs against gold SQL results.")
    parser.add_argument("--manifest", type=Path, default=Path("data/subset/manifest.json"))
    parser.add_argument("--predictions", type=Path, nargs="+", required=True)
    parser.add_argument("--output", type=Path, default=Path("data/outputs/metrics.jsonl"))
    parser.add_argument("--run-id", default="")
    args = parser.parse_args()

    settings = load_settings()
    examples = {example.example_id: example for example in load_manifest(args.manifest)}
    metrics = []
    for prediction_path in args.predictions:
        for record in read_jsonl(prediction_path):
            example = examples[record["example_id"]]
            metric = evaluate_record(record, example, settings.spider_data_dir)
            if args.run_id:
                metric["run_id"] = args.run_id
            metrics.append(metric)
    write_jsonl(args.output, metrics)
    print(f"Wrote {len(metrics)} metric records to {args.output}")


if __name__ == "__main__":
    main()
