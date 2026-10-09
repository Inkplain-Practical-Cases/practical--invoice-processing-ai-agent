# Why: return 404 on absent records while the provider owns all SQL.
from fastapi import HTTPException
from app.providers.database.session import get_db_session
from app.providers.database.invoice_repository import get_invoice

def handle_get_invoice(identifier:int)->dict:
    with get_db_session() as session:
        invoice = get_invoice(session,identifier)
    if invoice is None:
        raise HTTPException(status_code=404,detail="Invoice not found")
    return invoice
