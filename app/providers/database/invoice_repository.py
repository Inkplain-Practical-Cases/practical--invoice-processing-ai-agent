# Why: the repository owns a single transaction for invoice and child line items.
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.providers.database.models import InvoiceORM, InvoiceLineItemORM
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader

def save_invoice(session: Session, invoice: InvoiceHeader) -> dict:
    header = InvoiceORM(
        vendor=invoice.vendor, invoice_number=invoice.invoice_number,
        invoice_date=invoice.invoice_date, due_date=invoice.due_date, currency=invoice.currency,
        subtotal=invoice.subtotal, tax_amount=invoice.tax_amount, total_amount=invoice.total_amount)
    for item in invoice.items:
        header.items.append(InvoiceLineItemORM(
            description=item.description, quantity=item.quantity,
            unit_price=item.unit_price, line_total=item.line_total))
    try:
        session.add(header)
        session.commit()
        session.refresh(header)
        return {"id":header.id, **invoice.model_dump(mode="json")}
    except Exception:
        session.rollback()
        raise

def get_invoice(session:Session, identifier:int)->dict|None:
    invoice=session.scalar(select(InvoiceORM).options(selectinload(InvoiceORM.items)).where(InvoiceORM.id==identifier))
    if invoice is None:
        return None
    return {
        "id":invoice.id,"vendor":invoice.vendor,"invoice_number":invoice.invoice_number,
        "invoice_date":invoice.invoice_date.isoformat(),"due_date":invoice.due_date.isoformat(),
        "currency":invoice.currency,"subtotal":str(invoice.subtotal),"tax_amount":str(invoice.tax_amount),
        "total_amount":str(invoice.total_amount),
        "items":[{"description":x.description,"quantity":str(x.quantity),"unit_price":str(x.unit_price),
                  "line_total":str(x.line_total)} for x in invoice.items]
    }
