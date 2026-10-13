# STEP-5: Handle duplicates and processing errors

Add normalized vendor identity and PostgreSQL unique constraint; concurrent duplicate writes produce one HTTP 201 and one HTTP 409 with one persisted invoice. SQLAlchemy errors return safe 503. Run `docker compose up -d postgres && python -m pip install -r requirements.txt && python -m pytest -q`. Migration 002 upgrades an existing schema. STEP-6 adds safe logs and extended tests.

## Database (Entity) Relations
`STEP-5.erd` models the full PostgreSQL data in this branch: `invoices` and `invoice_line_items`, with line item foreign key `invoice_id -> invoices.id` (ON DELETE CASCADE). The invoices table adds vendor_normalized and a composite unique index; line items stay unchanged. The ERD appears as `STEP-5-ERD` in the main .inkp file. The schema follows the real SQL migrations and SQLAlchemy models.
