# Why: map SQL failures to stable HTTP status and emit only safe event metadata.
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader
from app.providers.database.session import get_db_session
from app.providers.database.invoice_repository import save_invoice
from app.core.observability import service_log_invoice_event

def service_save_invoice(invoice:InvoiceHeader)->dict:
    try:
        with get_db_session() as session:
            result = save_invoice(session,invoice)
        service_log_invoice_event("invoice_stored",result["id"],"success")
        return result
    except IntegrityError as exc:
        service_log_invoice_event("invoice_store_rejected",None,"duplicate")
        raise HTTPException(status_code=409,detail="Duplicate or conflicting invoice") from exc
    except SQLAlchemyError as exc:
        service_log_invoice_event("invoice_store_rejected",None,"unavailable")
        raise HTTPException(status_code=503,detail="Invoice storage unavailable") from exc
