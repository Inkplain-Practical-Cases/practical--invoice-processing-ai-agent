# Why: one place guarantees both math and calendar rules run before persistence.
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader
from app.features.invoice_validation.services.service_validate_invoice_amounts import service_validate_invoice_amounts
from app.features.invoice_validation.services.service_validate_invoice_dates import service_validate_invoice_dates

def service_validate_invoice(invoice: InvoiceHeader) -> InvoiceHeader:
    service_validate_invoice_amounts(invoice)
    service_validate_invoice_dates(invoice)
    return invoice
