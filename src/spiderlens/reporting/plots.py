from __future__ import annotations

import base64
from pathlib import Path


def write_metric_plot(records: list[dict], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "metric_summary.png"
    try:
        import matplotlib.pyplot as plt
    except ModuleNotFoundError:
        path.write_bytes(base64.b64decode(TINY_PNG))
        return path

    if not records:
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.text(0.5, 0.5, "No records available", ha="center", va="center")
        ax.axis("off")
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)
        return path

    metric_cols = ["cell_precision", "cell_recall", "tuple_cardinality"]
    grouped: dict[str, list[dict]] = {}
    for record in records:
        grouped.setdefault(str(record.get("pipeline", "unknown")), []).append(record)
    pipelines = sorted(grouped)
    values = []
    for pipeline in pipelines:
        items = grouped[pipeline]
        values.append([sum(float(item.get(metric, 0.0)) for item in items) / len(items) for metric in metric_cols])

    fig, ax = plt.subplots(figsize=(8, 4))
    width = 0.25
    x_positions = list(range(len(pipelines)))
    for metric_index, metric in enumerate(metric_cols):
        offsets = [x + (metric_index - 1) * width for x in x_positions]
        ax.bar(offsets, [row[metric_index] for row in values], width=width, label=metric)
    ax.set_xticks(x_positions, pipelines)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Score")
    ax.set_xlabel("Pipeline")
    ax.legend(loc="lower right")
    plt.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return path


TINY_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/p9sAAAAASUVORK5CYII="
)
