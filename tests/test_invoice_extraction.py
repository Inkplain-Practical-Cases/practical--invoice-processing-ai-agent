# Why: exercise real PDF files through the full FastAPI parsing endpoint.
from io import BytesIO
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from app.main import app

client = TestClient(app)
LINES = [
    "Vendor: Northstar Supplies",
    "Invoice No: INV-2026-0042",
    "Invoice Date: 2026-10-09",
    "Due Date: 2026-11-09",
    "Currency: EUR",
    "Item: Monitor | 3 | 300.00 | 900.00",
    "Subtotal: 900.00",
    "Tax: 171.00",
    "Total: 1071.00",
]

def make_pdf(lines: list[str]) -> bytes:
    buffer = BytesIO()
    doc = canvas.Canvas(buffer, pagesize=(610, 780))
    for i, line in enumerate(lines):
        doc.drawString(35, 740-i*25, line)
    doc.save()
    return buffer.getvalue()

def test_extracts_typed_invoice():
    result=client.post("/invoices/parse",files={"file":("invoice.pdf",make_pdf(LINES),"application/pdf")})
    assert result.status_code==200, result.text
    body=result.json()
    assert body["invoice_number"]=="INV-2026-0042"
    assert body["vendor"]=="Northstar Supplies"
    assert body["items"][0]["quantity"]=="3"
    assert body["total_amount"]=="1071.00"

def test_missing_invoice_number():
    result=client.post("/invoices/parse",files={"file":("invoice.pdf",make_pdf([x for x in LINES if not x.startswith("Invoice No:")]),"application/pdf")})
    assert result.status_code==422
    assert "invoice_number" in result.json()["detail"]["invalid_fields"]

def test_malformed_item():
    malformed=[x.replace(" | 3 | 300.00 | 900.00"," | bad") for x in LINES]
    result=client.post("/invoices/parse",files={"file":("invoice.pdf",make_pdf(malformed),"application/pdf")})
    assert result.status_code==422
