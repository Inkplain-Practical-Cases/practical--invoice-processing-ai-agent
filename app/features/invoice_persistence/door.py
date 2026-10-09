# Why: expose saved invoice query without mixing database logic into the HTTP layer.
from fastapi import APIRouter
from app.features.invoice_persistence.handlers.handle_get_invoice import handle_get_invoice

router=APIRouter(prefix="/invoices",tags=["Persistence"])

@router.get("/{identifier}")
def read_invoice(identifier:int)->dict:
    return handle_get_invoice(identifier)
