# Why: expose HTTP transport only; delegates PDF parsing to a handler.
from fastapi import APIRouter, File, UploadFile
from app.features.invoice_upload.handlers.handle_upload_invoice import handle_upload_invoice

router = APIRouter(prefix="/invoices", tags=["Invoices"])

@router.post("/extract")
async def extract_invoice(file: UploadFile = File(...)) -> dict:
    # Handler orchestrates reading and provider use.
    return await handle_upload_invoice(file)
