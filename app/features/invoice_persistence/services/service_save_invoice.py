# Why: convert predictable storage failures into safe HTTP errors, not SQL detail leaks.
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader
from app.providers.database.session import get_db_session
from app.providers.database.invoice_repository import save_invoice

def service_save_invoice(invoice:InvoiceHeader)->dict:
    try:
        with get_db_session() as session:
            return save_invoice(session,invoice)
    except IntegrityError as exc:
        # The unique database index is the authority, even for simultaneous writers.
        raise HTTPException(status_code=409,detail="Duplicate or conflicting invoice") from exc
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503,detail="Invoice storage unavailable") from exc
