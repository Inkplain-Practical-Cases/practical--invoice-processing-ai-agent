# Why: financial correctness must be deterministic, not an LLM opinion.
from decimal import Decimal
from fastapi import HTTPException
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader

CENT = Decimal("0.01")

def service_validate_invoice_amounts(invoice: InvoiceHeader) -> None:
    # Reject amounts that do not make financial sense.
    if any(x < 0 for x in (invoice.subtotal, invoice.tax_amount, invoice.total_amount)):
        raise HTTPException(status_code=422, detail="Negative totals are forbidden")
    if not invoice.items:
        raise HTTPException(status_code=422, detail="At least one item required")
    calculated = Decimal("0")
    for item in invoice.items:
        expected = (item.quantity * item.unit_price).quantize(CENT)
        if expected != item.line_total:
            raise HTTPException(status_code=422, detail="Invoice item arithmetic mismatch")
        calculated += expected
    if calculated.quantize(CENT) != invoice.subtotal:
        raise HTTPException(status_code=422, detail="Invoice subtotal mismatch")
    if (invoice.subtotal + invoice.tax_amount).quantize(CENT) != invoice.total_amount:
        raise HTTPException(status_code=422, detail="Invoice total mismatch")
