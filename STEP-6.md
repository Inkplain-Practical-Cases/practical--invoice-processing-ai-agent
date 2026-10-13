# STEP-6: Harden and verify

The final branch adds metadata-only structured logs and end-to-end upload→parse→validate→PostgreSQL→GET tests. It rejects corrupt/image-only PDFs, wrong totals and duplicates. CI must exercise all six cumulative branches and main; STEP-4 onward needs a PostgreSQL service. Run `docker compose up -d postgres && python -m pip install -r requirements.txt && python -m pytest -q`. Stage 3 will separately create the .inkp Simulator.

## Database (Entity) Relations
`STEP-6.erd` models the full PostgreSQL data in this branch: `invoices` and `invoice_line_items`, with line item foreign key `invoice_id -> invoices.id` (ON DELETE CASCADE). No schema changes are made; tables remain unchanged. The ERD appears as `STEP-6-ERD` in the main .inkp file. The schema follows the real SQL migrations and SQLAlchemy models.
