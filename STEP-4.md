# STEP-4: Integrate PostgreSQL storage

Adds SQLAlchemy invoice and child item ORM, database session provider, transaction-oriented repository, processing and read-only HTTP endpoints and Docker Compose. Run `docker compose up -d postgres`, install requirements and `python -m pytest -q`. The tests verify actual PostgreSQL parent/child persistence and 404 on missing invoice. STEP-5 adds a database unique key and safe error contracts.
