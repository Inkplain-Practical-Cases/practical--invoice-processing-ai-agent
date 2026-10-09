# Why: apply file validation then delegate text extraction; no PDF logic in the door.
from fastapi import UploadFile
from app.features.invoice_upload.services.service_validate_uploaded_pdf import service_validate_uploaded_pdf
from app.features.invoice_upload.services.service_extract_pdf_text import service_extract_pdf_text

async def handle_upload_invoice(file: UploadFile) -> dict:
    # Limit the streamed file read; never trust claimed content length.
    contents = await file.read(1024 * 1024 + 1)
    service_validate_uploaded_pdf(file.filename or "", contents)
    text = service_extract_pdf_text(contents)
    return {"filename": file.filename, "text": text}
