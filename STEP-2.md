# STEP-2: Extract structured invoice data

Read a synthetic PDF with known labeled fields; build typed InvoiceHeader/InvoiceLineItem objects. Missing required labels and malformed rows are explicit HTTP 422 results. Run `python -m pip install -r requirements.txt && python -m pytest -q`. This adds five new source components to the full CRD. The next step validates financial arithmetic.
