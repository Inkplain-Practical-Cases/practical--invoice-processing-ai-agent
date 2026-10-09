# Why: parse embedded PDF text without relying on remote APIs or model hallucination.
from io import BytesIO
from pypdf import PdfReader

def provider_extract_pdf_text(data: bytes) -> str:
    # The provider owns pypdf details and returns normalized text pages.
    reader = PdfReader(BytesIO(data), strict=False)
    return "\n".join((page.extract_text() or "") for page in reader.pages)
