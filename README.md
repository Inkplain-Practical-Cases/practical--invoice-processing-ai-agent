# Invoice Processing AI Agent — STEP-6

A cumulative real FastAPI document intake application:
- Accept up to 1MB real PDF uploads and read embedded text with pypdf.
- Parse a documented synthetic invoice format into typed invoice models.
- Verify EUR totals and dates deterministically with Decimal.
- Store valid invoice headers and lines in PostgreSQL via SQLAlchemy transactions.
- Reject duplicate normalized vendor + invoice_number by a database unique constraint.
- Return safe HTTP 409/503 and emit structured metadata-only audit events.

```bash
docker compose up -d postgres
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

POST /invoices/extract, POST /invoices/parse, POST /invoices/process and GET /invoices/{id} use independent ICS doors/handlers/services/providers.

Educational limitations: deterministic parser supports labeled text PDFs only; scanned pages require a later OCR adapter. Example database credentials are for local Docker only. No enterprise identity, financial approval, invoice payment, antivirus scanning or secure retention policy is implemented. Never use this version for sensitive real financial documents.
