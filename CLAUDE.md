# magic_cards_etl

Data pipeline for Magic: The Gathering card data (Scryfall bulk data, MTGJSON later),
orchestrated with Apache Airflow and organized as a medallion architecture.

## Architecture
- Bronze: raw files exactly as downloaded. Immutable. Stored in MinIO (S3-compatible).
- Silver: cleaned, deduplicated, typed data. Parquet files and PostgreSQL.
- Gold: analysis-ready tables.

## Layout
- `dags/`: Airflow DAG definitions only (orchestration).
- `etl/`: pure Python extract/transform/load functions. No Airflow imports.
- `tests/`, `scripts/`, `docs/`

## DAG conventions
- DAG files orchestrate; logic lives in `etl/`. No network calls, DB queries or heavy
  imports at module top level (Airflow re-parses DAG files constantly).
- Always set: dag_id, schedule, start_date, catchup=False, max_active_runs=1,
  default_args with retries and retry_delay, and tags.
- Pass references (paths/URIs) between tasks via XCom, never data.
- Read config from environment variables or Airflow Connections. Never hardcode.

## ETL conventions
- Idempotent: re-running a task for the same logical date gives the same result.
  Bronze writes go to date-partitioned paths; loads are upserts
  (INSERT ... ON CONFLICT) keyed on the Scryfall card id.
- Never modify Bronze. Silver must be reproducible from Bronze.
- Explicit schemas and types; no silent coercion.
- Data quality checks fail the task: non-empty input, unique ids, non-null keys.
- Scryfall: discover the bulk file via the bulk-data endpoint, send User-Agent and
  Accept headers, stay under 10 requests/second, and avoid re-downloading unchanged files.

## Code and tests
- Python with type hints; ruff for lint and format; `logging`, not `print`.
- pytest for `etl/` functions using small fixtures, plus a test that every DAG
  imports without errors.

## Git
- Conventional Commits; small commits, one concern each.
- Do not push unless asked. Never commit data files, venvs, logs or credentials.

## Security
- Never read, print, edit or commit `.env` or any credentials. Use `.env.example`
  with placeholders.
- No hardcoded secrets or default passwords in `docker-compose.yml`.
- Publish ports on 127.0.0.1 only.
- Ask before adding dependencies, installing system packages, or deleting files.
