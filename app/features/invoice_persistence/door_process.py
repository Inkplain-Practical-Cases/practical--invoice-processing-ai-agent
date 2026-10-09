# Why: process upload HTTP route delegates all extraction/storage to its handler.
from fastapi import APIRouter, File, UploadFile
from app.features.invoice_persistence.handlers.handle_process_invoice import handle_process_invoice

router=APIRouter(prefix="/invoices",tags=["Processing"])

@router.post("/process",status_code=201)
async def process_invoice(file:UploadFile=File(...))->dict:
    return await handle_process_invoice(file)
