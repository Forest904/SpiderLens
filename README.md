# SpiderLens

**SpiderLens** is a Python evaluation framework for comparing two LLM-based approaches to question answering over relational data:

1. **Text-to-SQL** - the model translates a natural-language question into SQL, which is executed on a SQLite database.
2. **Direct Table QA** - the model receives serialized table content and directly generates the answer.

The project is built for the *Models and Practice of Neural Table Representations* assignment and evaluates both paradigms on a small, curated subset of the Spider benchmark.

The goal is not to prove that one approach is universally better. Instead, SpiderLens characterizes the strengths, weaknesses, and failure modes of each method under a controlled experimental setup.

## Project Tracking

- [MILESTONES.md](MILESTONES.md) tracks the full assignment roadmap, acceptance criteria, and future work.
- [LAB_JOURNAL.md](LAB_JOURNAL.md) records trial-and-error runs, mistakes, metrics, and lessons learned.

## Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy the example environment file and fill in your local paths/API settings:

```powershell
Copy-Item .env.example .env
```

Expected environment variables:

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`
- `SPIDER_DATA_DIR`
- `SPIDERLENS_OUTPUT_DIR`

Raw Spider benchmark files should stay outside version control. Point `SPIDER_DATA_DIR` at a local Spider checkout containing files such as `dev.json` and `database/<db_id>/<db_id>.sqlite`.

## Project Overview

Given a natural-language question and its corresponding SQLite database, SpiderLens runs two independent pipelines.

### Text-to-SQL Pipeline

The model is prompted with:

- the natural-language question;
- the database schema;
- the oracle relevant tables.

It then generates a SQL query. The generated SQL is executed locally against the SQLite database, and the resulting output data is normalized for evaluation.

### Direct Table QA Pipeline

The system uses the oracle relevant tables, serializes their contents into text, appends the natural-language question, and prompts the model to directly return the answer.

The answer is parsed into a machine-readable format and normalized using the same logic as the Text-to-SQL output.

### Data-Centric Evaluation

Both pipelines are evaluated by comparing their output data against the ground-truth output data.

The first metrics are:

- **Cell Precision**
- **Cell Recall**
- **Tuple Cardinality**

Invalid SQL, execution errors, empty outputs, and unparsable model responses are treated as failed attempts.

## Workflow

Build or edit the manual subset manifest:

```powershell
python scripts/build_subset.py --spider-dir $env:SPIDER_DATA_DIR --limit 5
```

Then fill in `oracle_tables` in `data/subset/manifest.json`.

Run the two pipelines:

```powershell
python scripts/run_text_to_sql.py
python scripts/run_table_qa.py
```

Evaluate predictions:

```powershell
python scripts/evaluate.py --predictions data/outputs/text_to_sql.jsonl data/outputs/table_qa.jsonl
```

Generate report assets:

```powershell
python scripts/make_report_assets.py
```

Run tests:

```powershell
pytest
```

## Repository Structure

```text
SpiderLens/
|-- README.md
|-- requirements.txt
|-- .env.example
|-- data/
|   |-- subset/                  # Manual benchmark subset manifest
|   `-- outputs/                 # Ignored run outputs and caches
|-- src/spiderlens/
|   |-- config.py                # Environment configuration
|   |-- llm_client.py            # OpenAI-compatible cached LLM client
|   |-- dataset/                 # Spider loading, subset, schema utilities
|   |-- prompts/                 # Prompt templates
|   |-- pipelines/               # Text-to-SQL and Direct Table QA pipelines
|   |-- serialization/           # Table serialization formats
|   |-- execution/               # Safe SQLite execution
|   |-- parsing/                 # Model response parsing
|   |-- evaluation/              # Normalization, metrics, comparison
|   |-- analysis/                # Failure labels
|   `-- reporting/               # Markdown tables and plots
|-- scripts/                     # Runnable command-line scripts
|-- tests/                       # Unit and fixture-based tests
|-- notebooks/                   # Optional exploratory notebooks
`-- report/
    |-- figures/
    `-- tables/
```
