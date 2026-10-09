# Why: a read-only query must report absence safely without exposing database errors.
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from app.providers.database.session import get_db_session
from app.providers.database.invoice_repository import get_invoice

def handle_get_invoice(identifier:int)->dict:
    try:
        with get_db_session() as session:
            invoice=get_invoice(session,identifier)
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=503,detail="Invoice storage unavailable") from exc
    if invoice is None:
        raise HTTPException(status_code=404,detail="Invoice not found")
    return invoice
