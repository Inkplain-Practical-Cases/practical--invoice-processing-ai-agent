# Why: HTTP path is an adapter, not a home for parsing rules.
from fastapi import APIRouter, File, UploadFile
from app.features.invoice_extraction.handlers.handle_parse_invoice import handle_parse_invoice

router = APIRouter(prefix="/invoices", tags=["Invoice parsing"])

@router.post("/parse")
async def parse_invoice(file: UploadFile = File(...)) -> dict:
    return await handle_parse_invoice(file)
