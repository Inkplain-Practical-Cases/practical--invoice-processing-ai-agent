# Invoice Processing AI Agent — STEP 2
Extends working STEP-1 PDF upload with deterministic parsing of synthetic text-layer invoice documents.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --reload
```

POST /invoices/parse with a PDF containing labeled lines: Vendor, Invoice No, Invoice Date, Due Date, Currency, Item, Subtotal, Tax and Total. The Item line is `Item: description | qty | unit price | line total`. Invalid fields are reported, not invented. Financial arithmetic validation begins in STEP-3.
