# Why: keep PDF engine behind one replaceable service boundary.
from fastapi import HTTPException
from app.providers.pdf.provider_extract_pdf_text import provider_extract_pdf_text

def service_extract_pdf_text(data: bytes) -> str:
    try:
        text = provider_extract_pdf_text(data)
    except Exception as exc:
        # Do not disclose parser internals or document text to the client.
        raise HTTPException(status_code=422, detail="Unreadable PDF") from exc
    if not text.strip():
        raise HTTPException(status_code=422, detail="PDF has no extractable text")
    return text
