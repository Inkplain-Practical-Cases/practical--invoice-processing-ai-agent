# Why: validate parsed invoice before reporting it accepted.
from fastapi import UploadFile
from app.features.invoice_upload.handlers.handle_upload_invoice import handle_upload_invoice
from app.features.invoice_extraction.services.service_parse_invoice_text import service_parse_invoice_text
from app.features.invoice_validation.services.service_validate_invoice import service_validate_invoice

async def handle_parse_invoice(file: UploadFile) -> dict:
    extracted = await handle_upload_invoice(file)
    invoice = service_parse_invoice_text(extracted["text"])
    service_validate_invoice(invoice)
    return invoice.model_dump(mode="json")
