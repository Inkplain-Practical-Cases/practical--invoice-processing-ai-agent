# Why: exercise real FastAPI multipart routing, file-type checks and pypdf extraction.
from io import BytesIO
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from app.main import app

client = TestClient(app)

def pdf_of(text: str) -> bytes:
    # Create text-layer fixtures with no remote documents.
    buf = BytesIO()
    doc = canvas.Canvas(buf, pagesize=(600, 600))
    doc.drawString(40, 550, text)
    doc.save()
    return buf.getvalue()

def test_valid_pdf_upload() -> None:
    response = client.post("/invoices/extract", files={"file": ("invoice.pdf", pdf_of("INV-42 Supplier"), "application/pdf")})
    assert response.status_code == 200
    assert "INV-42" in response.json()["text"]

def test_wrong_extension_and_signature() -> None:
    pdf = pdf_of("document")
    assert client.post("/invoices/extract", files={"file": ("x.txt", pdf, "application/pdf")}).status_code == 415
    assert client.post("/invoices/extract", files={"file": ("x.pdf", b"not a PDF", "application/pdf")}).status_code == 415

def test_corrupt_pdf() -> None:
    response = client.post("/invoices/extract", files={"file": ("x.pdf", b"%PDF-this-is-not-valid", "application/pdf")})
    assert response.status_code == 422

def test_oversized_pdf() -> None:
    result = client.post("/invoices/extract", files={"file": ("x.pdf", b"%PDF-" + b"x" * (1024*1024), "application/pdf")})
    assert result.status_code == 413
