"""Extract: download raw source files into Bronze.

Discovers the Scryfall bulk file via the bulk-data endpoint and writes it unchanged
to a date-partitioned path in MinIO. Implemented in Phase 2.
"""
