# Run Summary: run_0001

- Timestamp: `2026-05-01_140701`
- Manifest: `data\subset\manifest.json`
- Model: `gpt-4o-mini`
- Base URL: `https://api.openai.com/v1`
- Temperature: `0.0`
- Prompt strategy: `zero_shot_text_to_sql_and_direct_table_qa`
- Serialization strategy: `markdown_table_for_table_qa`
- Text-to-SQL records: `3`
- Table QA records: `3`
- Metric records: `6`

## Reproduction Commands

```powershell
.\.venv\Scripts\python.exe scripts\run_experiment.py --manifest data\subset\manifest.json --run-id run_0001 --baseline-metrics data\outputs\runs\run_0000\metrics.jsonl
```

## Aggregate Metrics

| pipeline | records | cell_precision | cell_recall | tuple_cardinality |
| --- | --- | --- | --- | --- |
| table_qa | 3 | 0.6746 | 1.0 | 0.7222 |
| text_to_sql | 3 | 1.0 | 1.0 | 1.0 |

## Failure Counts

| pipeline | failure_label | db_id | query_pattern | count |
| --- | --- | --- | --- | --- |
| table_qa | success | concert_singer | unknown | 3 |
| text_to_sql | success | concert_singer | unknown | 3 |

## Metric Deltas

| pipeline | cell_precision_current | cell_precision_baseline | cell_precision_delta | cell_recall_current | cell_recall_baseline | cell_recall_delta | tuple_cardinality_current | tuple_cardinality_baseline | tuple_cardinality_delta |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| table_qa | 0.6746 | 0.6746 | 0.0 | 1.0 | 1.0 | 0.0 | 0.7222 | 0.7222 | 0.0 |
| text_to_sql | 1.0 | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 | 1.0 | 1.0 | 0.0 |

## Artifacts

- [summary](summary.md)
- [per-example metrics](per_example_metrics.md)
- [failure breakdown](failure_breakdown.md)
- [metric deltas](metric_deltas.md)
- [metric plot](metric_summary.png)
- [run journal](lab_journal.md)
- [metadata](metadata.json)
