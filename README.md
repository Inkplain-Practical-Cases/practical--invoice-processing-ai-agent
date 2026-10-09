# Invoice Processing AI Agent — STEP 5

Adds a PostgreSQL UNIQUE constraint on normalized vendor plus invoice_number, and maps duplicate insert races to safe HTTP 409 responses. SQLAlchemy storage failures return HTTP 503 without exposing SQL or PDF contents. An existing database can run migration SQL in migrations/002_invoice_unique_key.sql after duplicate cleanup. Run `docker compose up -d postgres`, install requirements and `python -m pytest -q`.
