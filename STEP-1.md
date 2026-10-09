# STEP-1: Receive and read PDF invoices
## What you build
An independently runnable FastAPI multipart PDF upload, bounded validation and a pypdf text extraction provider.
## How
Thin door → handler → validation service → PDF text service → library adapter.
## Verification
Run `python -m pip install -r requirements.txt && python -m pytest -q`.
Test legitimate generated PDF text, bad signatures and extensions, oversized and corrupt uploads.
## Next
Extract structured header/line items from supported synthetic text.
