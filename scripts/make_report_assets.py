from __future__ import annotations

import argparse
from pathlib import Path

from _bootstrap import add_src_to_path

add_src_to_path()


def main() -> None:
    from spiderlens.io import read_jsonl
    from spiderlens.reporting.plots import write_metric_plot
    from spiderlens.reporting.tables import write_summary_tables

    parser = argparse.ArgumentParser(description="Generate Markdown tables and figures from metric JSONL.")
    parser.add_argument("--metrics", type=Path, default=Path("data/outputs/metrics.jsonl"))
    parser.add_argument("--tables-dir", type=Path, default=Path("report/tables"))
    parser.add_argument("--figures-dir", type=Path, default=Path("report/figures"))
    args = parser.parse_args()

    records = read_jsonl(args.metrics)
    table_paths = write_summary_tables(records, args.tables_dir)
    plot_path = write_metric_plot(records, args.figures_dir)
    print("Wrote report assets:")
    for name, path in table_paths.items():
        print(f"- {name}: {path}")
    print(f"- plot: {plot_path}")


if __name__ == "__main__":
    main()
