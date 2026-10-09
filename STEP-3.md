# STEP-3: Validate invoice business rules

Added Decimal math, line/subtotal/tax/total consistency, due-date and supported EUR currency rules. The parse handler now verifies before returning success. Run `python -m pip install -r requirements.txt && python -m pytest -q`; inspect `tests/test_invoice_validation.py`. STEP-4 introduces PostgreSQL persistence.
