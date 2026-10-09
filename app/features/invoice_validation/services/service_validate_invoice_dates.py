# Why: a due date before an issue date is an invalid business record.
from fastapi import HTTPException
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader

def service_validate_invoice_dates(invoice: InvoiceHeader) -> None:
    if invoice.due_date < invoice.invoice_date:
        raise HTTPException(status_code=422, detail="Due date precedes invoice date")
    if invoice.currency != "EUR":
        # This teaching case fixes one supported currency for unambiguous tests.
        raise HTTPException(status_code=422, detail="Only EUR is supported")
