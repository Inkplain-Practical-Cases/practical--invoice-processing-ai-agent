# STEP-5: Handle duplicates and processing errors

Add normalized vendor identity and PostgreSQL unique constraint; concurrent duplicate writes produce one HTTP 201 and one HTTP 409 with one persisted invoice. SQLAlchemy errors return safe 503. Run `docker compose up -d postgres && python -m pip install -r requirements.txt && python -m pytest -q`. Migration 002 upgrades an existing schema. STEP-6 adds safe logs and extended tests.
