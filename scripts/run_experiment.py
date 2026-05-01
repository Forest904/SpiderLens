from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.config import load_settings
    from spiderlens.dataset.subset import load_manifest
    from spiderlens.evaluation.compare import evaluate_record
    from spiderlens.io import write_jsonl
    from spiderlens.llm_client import CachedLLMClient, LLMConfig
    from spiderlens.pipelines.table_qa import run_example as run_table_qa_example
    from spiderlens.pipelines.text_to_sql import run_example as run_text_to_sql_example
    from spiderlens.reporting.run_report import write_run_report
    from spiderlens.reporting.runs import next_run_id, validate_run_id

    parser = argparse.ArgumentParser(description="Run both SpiderLens pipelines and create run-scoped report assets.")
    parser.add_argument("--manifest", type=Path, default=Path("data/subset/manifest.json"))
    parser.add_argument("--outputs-dir", type=Path, default=Path("data/outputs/runs"))
    parser.add_argument("--report-runs-dir", type=Path, default=Path("report/runs"))
    parser.add_argument("--run-id", default="")
    parser.add_argument("--baseline-metrics", type=Path)
    parser.add_argument("--refresh-cache", action="store_true")
    args = parser.parse_args()

    settings = load_settings()
    run_id = validate_run_id(args.run_id) if args.run_id else next_run_id(args.report_runs_dir)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_output_dir = args.outputs_dir / run_id
    text_to_sql_path = run_output_dir / "text_to_sql.jsonl"
    table_qa_path = run_output_dir / "table_qa.jsonl"
    metrics_path = run_output_dir / "metrics.jsonl"

    llm_config = LLMConfig(settings.llm_api_key, settings.llm_base_url, settings.llm_model, settings.temperature)
    client = CachedLLMClient(llm_config, settings.spiderlens_output_dir / "cache")
    examples = load_manifest(args.manifest)

    text_to_sql_records = [
        run_text_to_sql_example(example, settings.spider_data_dir, client, args.refresh_cache, run_id)
        for example in examples
    ]
    table_qa_records = [
        run_table_qa_example(example, settings.spider_data_dir, client, args.refresh_cache, run_id)
        for example in examples
    ]
    write_jsonl(text_to_sql_path, text_to_sql_records)
    write_jsonl(table_qa_path, table_qa_records)

    examples_by_id = {example.example_id: example for example in examples}
    metric_records = []
    for record in [*text_to_sql_records, *table_qa_records]:
        metric_records.append(evaluate_record(record, examples_by_id[record["example_id"]], settings.spider_data_dir))
    write_jsonl(metrics_path, metric_records)

    commands = [
        (
            f".\\.venv\\Scripts\\python.exe scripts\\run_experiment.py --manifest {args.manifest} "
            f"--run-id {run_id}"
        )
    ]
    if args.baseline_metrics:
        commands[0] += f" --baseline-metrics {args.baseline_metrics}"
    metadata = {
        "run_id": run_id,
        "timestamp": timestamp,
        "date": timestamp.split("_")[0],
        "manifest_path": str(args.manifest),
        "model": settings.llm_model,
        "base_url": settings.llm_base_url,
        "temperature": settings.temperature,
        "prompt_strategy": "zero_shot_text_to_sql_and_direct_table_qa",
        "serialization_strategy": "markdown_table_for_table_qa",
        "record_counts": {
            "text_to_sql": len(text_to_sql_records),
            "table_qa": len(table_qa_records),
            "metrics": len(metric_records),
        },
        "prediction_paths": {
            "text_to_sql": str(text_to_sql_path),
            "table_qa": str(table_qa_path),
            "metrics": str(metrics_path),
        },
        "commands": commands,
    }
    report_paths = write_run_report(
        metric_records,
        args.report_runs_dir,
        run_id,
        timestamp,
        metadata,
        args.baseline_metrics,
    )

    print(f"Run ID: {run_id}")
    print(f"Wrote predictions and metrics under {run_output_dir}")
    print("Wrote report assets:")
    for name, path in report_paths.items():
        print(f"- {name}: {path}")


if __name__ == "__main__":
    main()
