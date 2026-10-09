# Invoice Processing AI Agent — STEP 3

PDF upload and typed parsing now pass through deterministic financial validation. The service uses Decimal for line totals, subtotal, tax and total, and rejects a due date before an invoice date or a currency other than EUR. No database is required through STEP-3.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.
