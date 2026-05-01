from spiderlens.reporting.plots import write_metric_plot
from spiderlens.reporting.run_report import write_run_report
from spiderlens.reporting.runs import next_run_id
from spiderlens.reporting.tables import write_summary_tables


def test_next_run_id_autoincrements_and_ignores_nonmatching_dirs(tmp_path) -> None:
    runs_dir = tmp_path / "runs"

    assert next_run_id(runs_dir) == "run_0001"

    (runs_dir / "run_0001").mkdir(parents=True)
    (runs_dir / "run_0002").mkdir()
    (runs_dir / "notes").mkdir()
    (runs_dir / "run_latest").mkdir()

    assert next_run_id(runs_dir) == "run_0003"


def test_report_assets_are_written(tmp_path) -> None:
    records = [
        {
            "pipeline": "text_to_sql",
            "status": "ok",
            "cell_precision": 1.0,
            "cell_recall": 1.0,
            "tuple_cardinality": 1.0,
        }
    ]

    table_paths = write_summary_tables(records, tmp_path / "tables")
    plot_path = write_metric_plot(records, tmp_path / "figures")

    assert table_paths["summary"].exists()
    assert plot_path.exists()


def test_run_report_writes_run_scoped_assets_and_failed_records(tmp_path) -> None:
    records = [
        {
            "run_id": "run_0001",
            "pipeline": "text_to_sql",
            "example_id": "dev-0001",
            "db_id": "concert_singer",
            "query_pattern": "aggregation",
            "status": "ok",
            "failure_label": "success",
            "cell_precision": 1.0,
            "cell_recall": 1.0,
            "tuple_cardinality": 1.0,
            "error": "",
        },
        {
            "run_id": "run_0001",
            "pipeline": "table_qa",
            "example_id": "dev-0001",
            "db_id": "concert_singer",
            "query_pattern": "aggregation",
            "status": "failed",
            "failure_label": "parse_error",
            "cell_precision": 0.0,
            "cell_recall": 0.0,
            "tuple_cardinality": 0.0,
            "error": "JSON parse failed",
        },
    ]
    baseline_path = tmp_path / "baseline.jsonl"
    baseline_path.write_text(
        "\n".join(
            [
                '{"pipeline": "text_to_sql", "cell_precision": 0.5, "cell_recall": 1.0, "tuple_cardinality": 1.0}',
                '{"pipeline": "table_qa", "cell_precision": 0.25, "cell_recall": 0.5, "tuple_cardinality": 0.75}',
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    metadata = {
        "run_id": "run_0001",
        "timestamp": "2026-05-01_153000",
        "date": "2026-05-01",
        "manifest_path": "data/subset/manifest.json",
        "model": "gpt-4o-mini",
        "base_url": "https://api.openai.com/v1",
        "temperature": 0.0,
        "prompt_strategy": "zero_shot",
        "serialization_strategy": "markdown_table",
        "record_counts": {"text_to_sql": 1, "table_qa": 1, "metrics": 2},
        "commands": [".\\.venv\\Scripts\\python.exe scripts\\run_experiment.py --run-id run_0001"],
    }

    paths = write_run_report(
        records,
        tmp_path / "report" / "runs",
        "run_0001",
        "2026-05-01_153000",
        metadata,
        baseline_path,
    )

    assert paths["summary"].exists()
    assert paths["summary_timestamped"].exists()
    assert paths["plot"].exists()

    per_example = paths["per_example"].read_text(encoding="utf-8")
    assert "parse_error" in per_example
    assert "JSON parse failed" in per_example

    failures = paths["failures"].read_text(encoding="utf-8")
    assert "| table_qa | parse_error | concert_singer | aggregation | 1 |" in failures

    deltas = paths["deltas"].read_text(encoding="utf-8")
    assert "cell_precision_delta" in deltas
    assert "| text_to_sql | 1.0 | 0.5 | 0.5 |" in deltas

    summary = paths["summary"].read_text(encoding="utf-8")
    assert "Run Summary: run_0001" in summary
    assert "scripts\\run_experiment.py --run-id run_0001" in summary
