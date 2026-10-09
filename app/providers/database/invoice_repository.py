# Why: the database transaction and unique constraint protect concurrent inserts.
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from app.providers.database.models import InvoiceORM, InvoiceLineItemORM
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader
from app.features.invoice_persistence.services.service_normalize_vendor import service_normalize_vendor

def save_invoice(session:Session,invoice:InvoiceHeader)->dict:
    header=InvoiceORM(vendor=invoice.vendor,
        vendor_normalized=service_normalize_vendor(invoice.vendor),
        invoice_number=invoice.invoice_number, invoice_date=invoice.invoice_date,
        due_date=invoice.due_date,currency=invoice.currency,subtotal=invoice.subtotal,
        tax_amount=invoice.tax_amount,total_amount=invoice.total_amount)
    for item in invoice.items:
        header.items.append(InvoiceLineItemORM(
            description=item.description,quantity=item.quantity,
            unit_price=item.unit_price,line_total=item.line_total))
    try:
        session.add(header)
        session.commit()
        session.refresh(header)
        return {"id":header.id,**invoice.model_dump(mode="json")}
    except Exception:
        session.rollback()
        raise

def get_invoice(session:Session,identifier:int)->dict|None:
    record=session.scalar(select(InvoiceORM).options(selectinload(InvoiceORM.items)).where(InvoiceORM.id==identifier))
    if record is None:
        return None
    return {"id":record.id,"vendor":record.vendor,"invoice_number":record.invoice_number,
            "invoice_date":record.invoice_date.isoformat(),"due_date":record.due_date.isoformat(),
            "currency":record.currency,"subtotal":str(record.subtotal),
            "tax_amount":str(record.tax_amount),"total_amount":str(record.total_amount),
            "items":[{"description":x.description,"quantity":str(x.quantity),
                      "unit_price":str(x.unit_price),"line_total":str(x.line_total)} for x in record.items]}
