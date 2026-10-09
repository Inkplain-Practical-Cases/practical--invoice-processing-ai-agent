# Invoice Processing AI Agent

**Inkplain Practical Case 4/6 — Starter Forward Deployed Engineering.**

This runnable educational Python/FastAPI application receives text-based PDF invoices, extracts embedded text, deterministically parses a documented synthetic invoice format, validates EUR financial calculations using Decimal, and transactionally persists headers and line items to PostgreSQL. It refuses duplicate normalized vendor/invoice-number combinations through a database unique constraint.

## Quick start (Python 3.12+)
```bash
git clone https://github.com/Inkplain-Practical-Cases/practical--invoice-processing-ai-agent.git
cd practical--invoice-processing-ai-agent
docker compose up -d postgres
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000/docs. An invoice must contain actual embedded PDF text. A scanned-only PDF cannot be extracted without an OCR adapter.

## Supported synthetic invoice format

```text
Vendor: Northstar Supplies
Invoice No: INV-2026-0042
Invoice Date: 2026-10-09
Due Date: 2026-11-09
Currency: EUR
Item: Monitor | 3 | 300.00 | 900.00
Subtotal: 900.00
Tax: 171.00
Total: 1071.00
```

Generate PDFs containing those lines with ReportLab (see tests). File-size cap is 1 MiB and the PDF signature and extension are checked. The parser is not intended to read arbitrary invoice layouts, does not guess missing fields and does not use a paid model service.

## API
- `POST /invoices/extract` → PDF text.
- `POST /invoices/parse` → typed and financially validated invoice JSON.
- `POST /invoices/process` → transactional PostgreSQL write (HTTP 201), safe duplicate HTTP 409, validation HTTP 422, storage failure HTTP 503.
- `GET /invoices/{id}` → persisted header and line items, or HTTP 404.

## Learning branches
1. `step-01-receive-and-read-pdf-invoices`: validated PDF upload, pypdf provider.
2. `step-02-extract-structured-invoice-data`: deterministic parser, typed invoice and line items.
3. `step-03-validate-invoice-business-rules`: Decimal math, date and EUR checks.
4. `step-04-integrate-postgresql-storage`: SQLAlchemy 2, PostgreSQL transaction, read API.
5. `step-05-handle-duplicates-and-processing-errors`: unique normalized vendor/invoice key, safe 409/503.
6. `step-06-harden-and-verify`: safe events, corrupt PDF and end-to-end tests.

Each cumulative step branch has its own `STEP-N.crd` and `STEP-N.md`, and runnable pytest suite. The final main branch has `FINAL.crd`, this README and CI workflow. Stage 3 is separately responsible for `invoice-processing-ai-agent.inkp` (6 tab Simulator).

## Architecture
Inkplain Codebase Structure: thin FastAPI doors → feature handlers → services → isolated PDF and PostgreSQL providers; ORM session owns transaction and rollback. `migrations/001_create_invoice_tables.sql` and `002_invoice_unique_key.sql` document database schema history; unit/integration tests use clean schema fixtures via SQLAlchemy metadata against a disposable PostgreSQL database.

## CI and correctness
The GitHub Actions seven-branch pytest matrix uses Python 3.12; STEP-4 through main exercise actual PostgreSQL service. Verify CI job conclusions before claiming release success.

## Important security boundaries
This repository is for synthetic offline training, NOT for real supplier invoices or financial approvals. Docker credentials are local demo fixtures only. No login, malware scanning, secure document retention, OCR, LLM financial judgment or payment processing is provided. Sensitive documents require authenticated access, scanning, encryption and regulated storage policies before production use.
