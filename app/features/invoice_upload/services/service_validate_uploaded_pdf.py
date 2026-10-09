# Why: stop malformed, overly large or non-PDF bytes before reaching the PDF library.
from fastapi import HTTPException

MAX_PDF_BYTES = 1024 * 1024

def service_validate_uploaded_pdf(filename: str, data: bytes) -> None:
    # Both the extension and actual file header must indicate a PDF.
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="PDF extension required")
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=415, detail="Invalid PDF signature")
    if len(data) > MAX_PDF_BYTES:
        raise HTTPException(status_code=413, detail="PDF exceeds one megabyte")
