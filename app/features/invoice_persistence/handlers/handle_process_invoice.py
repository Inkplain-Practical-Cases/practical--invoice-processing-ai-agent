# Why: orchestrate extraction, parsing, validation then save only valid invoice data.
from fastapi import UploadFile
from app.features.invoice_upload.handlers.handle_upload_invoice import handle_upload_invoice
from app.features.invoice_extraction.services.service_parse_invoice_text import service_parse_invoice_text
from app.features.invoice_validation.services.service_validate_invoice import service_validate_invoice
from app.features.invoice_persistence.services.service_save_invoice import service_save_invoice

async def handle_process_invoice(file:UploadFile)->dict:
    text= (await handle_upload_invoice(file))["text"]
    invoice=service_validate_invoice(service_parse_invoice_text(text))
    return service_save_invoice(invoice)
