# Invoice Processing AI Agent — STEP 1

This cumulative teaching branch exposes a real FastAPI PDF extraction endpoint.
The thin door delegates to a handler, upload validation and a pypdf provider.
Scanned-only PDFs do not contain embedded text and are rejected.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

Try POST /invoices/extract from /docs with a text-layer PDF. No external services, API keys, payments or OCR.
