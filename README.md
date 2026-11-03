# magic_cards_etl

Data pipeline for Magic: The Gathering card data. It ingests
[Scryfall](https://scryfall.com/docs/api/bulk-data) bulk data (and
[MTGJSON](https://mtgjson.com/) price history later), orchestrated with Apache Airflow
and organized as a medallion architecture.

> Status: Phase 0 (repo hygiene). No pipeline code yet.

## Architecture

| Layer  | Contents                                          | Storage                 |
|--------|---------------------------------------------------|-------------------------|
| Bronze | Raw files exactly as downloaded. Immutable.       | MinIO (S3-compatible)   |
| Silver | Cleaned, deduplicated, typed data.                | Parquet and PostgreSQL  |
| Gold   | Analysis-ready tables.                            | PostgreSQL              |

Silver is always reproducible from Bronze, and every task is idempotent for a given
logical date.

## Repository layout

```
dags/      Airflow DAG definitions (orchestration only)
etl/       Pure Python extract/transform/load functions (no Airflow imports)
tests/     pytest tests for etl/ and a DAG import test
scripts/   Helper scripts
docs/      Project documentation
```

## Setup

Requires Python 3.12+ and [pipx](https://pipx.pypa.io/).

```bash
# Git hooks: gitleaks (secret detection) and ruff (lint and format)
pipx install pre-commit
pre-commit install
pre-commit run --all-files

# Local configuration
cp .env.example .env   # then fill in the values; .env is git-ignored
```

## Roadmap

| Phase | Scope                                                        |
|-------|--------------------------------------------------------------|
| 0     | Repo hygiene                                                 |
| 1     | Docker infrastructure (Airflow, PostgreSQL, MinIO)           |
| 2     | Bronze ingestion (Scryfall bulk)                             |
| 3     | Silver                                                       |
| 4     | Gold                                                         |
| 5     | Tests, data quality and CI (GitHub Actions)                  |
| 6     | MTGJSON price history                                        |
| 7     | AI layer (pgvector embeddings + read-only SQL agent)         |
| 8     | Optional: price model, real S3                               |
