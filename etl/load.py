"""Load: write Silver data into PostgreSQL.

Upserts (INSERT ... ON CONFLICT) keyed on the Scryfall card id so re-runs are
idempotent. Implemented in Phase 3.
"""
