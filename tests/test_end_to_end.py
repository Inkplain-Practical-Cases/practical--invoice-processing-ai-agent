# Why: verify upload, parse, validate, durable write, lookup and safe failure outcomes.
from io import BytesIO
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from app.main import app
client=TestClient(app)

VALID=[
    "Vendor: Northstar Supplies","Invoice No: INV-2026-0042",
    "Invoice Date: 2026-10-09","Due Date: 2026-11-09","Currency: EUR",
    "Item: Monitor | 3 | 300.00 | 900.00",
    "Subtotal: 900.00","Tax: 171.00","Total: 1071.00",
]

def build(lines:list[str])->bytes:
    buffer=BytesIO()
    doc=canvas.Canvas(buffer)
    for i,line in enumerate(lines): doc.drawString(35,760-24*i,line)
    doc.save()
    return buffer.getvalue()

def send(data:bytes):
    return client.post("/invoices/process",files={"file":("invoice.pdf",data,"application/pdf")})

def test_complete_document_workflow():
    result=send(build(VALID))
    assert result.status_code==201, result.text
    invoice_id=result.json()["id"]
    fetched=client.get(f"/invoices/{invoice_id}")
    assert fetched.status_code==200
    assert fetched.json()["total_amount"]=="1071.00"
    assert len(fetched.json()["items"])==1
    assert send(build(VALID)).status_code==409

def test_bad_arithmetic_never_persists():
    wrong=[x.replace("Total: 1071.00","Total: 1072.00") for x in VALID]
    assert send(build(wrong)).status_code==422
    assert send(build(VALID)).status_code==201

def test_corrupt_and_image_only_pdf_not_processed():
    assert send(b"%PDF-broken").status_code==422
    assert send(build([])).status_code==422
