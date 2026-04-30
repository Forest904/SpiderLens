from spiderlens.reporting.plots import write_metric_plot
from spiderlens.reporting.tables import write_summary_tables


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
