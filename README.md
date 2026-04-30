# SpiderLens

**SpiderLens** is a Python evaluation framework for comparing two LLM-based approaches to question answering over relational data:

1. **Text-to-SQL** — the model translates a natural-language question into SQL, which is executed on a SQLite database.
2. **Direct Table QA** — the model receives serialized table content and directly generates the answer.

The project is built for the *Models and Practice of Neural Table Representations* assignment and evaluates both paradigms on a small, curated subset of the Spider benchmark.

The goal is not to prove that one approach is universally better. Instead, SpiderLens aims to characterize the strengths, weaknesses, and failure modes of each method under a controlled experimental setup.

---

## Project Overview

Given a natural-language question and its corresponding SQLite database, SpiderLens runs two independent pipelines:

### 1. Text-to-SQL Pipeline

The model is prompted with:

- the natural-language question;
- the database schema;
- the oracle relevant tables.

It then generates a SQL query. The generated SQL is executed locally against the SQLite database, and the resulting output data is normalized for evaluation.

### 2. Direct Table QA Pipeline

The system uses the oracle relevant tables, serializes their contents into text, appends the natural-language question, and prompts the model to directly return the answer.

The answer is parsed into a machine-readable format and normalized using the same logic as the Text-to-SQL output.

### 3. Data-Centric Evaluation

Both pipelines are evaluated by comparing their output data against the ground-truth output data.

The main metrics are:

- **Cell Precision**
- **Cell Recall**
- **Tuple Cardinality**

Optional metrics may include:

- **Tuple Constraint**
- **Tuple Order**

Invalid SQL, execution errors, empty outputs, and unparsable model responses are treated as failed attempts.

---

## Repository Structure

```text
SpiderLens/
│
├── README.md
├── requirements.txt
├── .env.example
│
├── data/
│   ├── spider/                     # Spider benchmark files and SQLite databases
│   ├── subset/                     # Selected benchmark subset
│   └── outputs/                    # Raw outputs, predictions, metrics
│
├── src/
│   ├── config.py                   # Project configuration
│   ├── llm_client.py               # LLM API wrapper
│   │
│   ├── dataset/
│   │   ├── load_spider.py          # Spider loading utilities
│   │   ├── subset.py               # Subset construction
│   │   └── schema.py               # Schema extraction utilities
│   │
│   ├── prompts/
│   │   ├── text_to_sql.py          # Text-to-SQL prompt templates
│   │   └── table_qa.py             # Direct Table QA prompt templates
│   │
│   ├── pipelines/
│   │   ├── text_to_sql.py          # Text-to-SQL pipeline
│   │   └── table_qa.py             # Direct Table QA pipeline
│   │
│   ├── serialization/
│   │   ├── markdown.py             # Markdown table serialization
│   │   ├── json_rows.py            # JSON row serialization
│   │   └── compact.py              # Compact row-wise serialization
│   │
│   ├── execution/
│   │   └── sqlite_runner.py        # Safe SQLite execution
│   │
│   ├── parsing/
│   │   ├── sql_output.py           # SQL extraction from model output
│   │   └── answer_output.py        # Direct QA answer parsing
│   │
│   ├── evaluation/
│   │   ├── normalize.py            # Output normalization
│   │   ├── metrics.py              # Evaluation metrics
│   │   └── compare.py              # Prediction vs. ground truth comparison
│   │
│   ├── analysis/
│   │   └── failure_labels.py       # Failure type classification
│   │
│   └── reporting/
│       ├── tables.py               # Result table generation
│       └── plots.py                # Plot generation
│
├── scripts/
│   ├── build_subset.py
│   ├── run_text_to_sql.py
│   ├── run_table_qa.py
│   ├── evaluate.py
│   └── make_report_assets.py
│
├── notebooks/
│   ├── 01_explore_spider.ipynb
│   ├── 02_prompt_debugging.ipynb
│   └── 03_error_analysis.ipynb
│
├── tests/
│   ├── test_normalize.py
│   ├── test_metrics.py
│   └── test_sql_runner.py
│
└── report/
    ├── figures/
    ├── tables/
    └── report.pdf
