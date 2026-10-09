# Why: exercise exact Decimal boundaries and date rule in a real HTTP upload.
from io import BytesIO
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from app.main import app

client=TestClient(app)
LINES=["Vendor: Northstar Supplies","Invoice No: INV-2026-0042",
       "Invoice Date: 2026-10-09","Due Date: 2026-11-09","Currency: EUR",
       "Item: Monitor | 3 | 300.00 | 900.00",
       "Subtotal: 900.00","Tax: 171.00","Total: 1071.00"]

def pdf(lines:list[str])->bytes:
    buf=BytesIO()
    c=canvas.Canvas(buf)
    for i,line in enumerate(lines):
        c.drawString(30,750-i*24,line)
    c.save()
    return buf.getvalue()

def upload(lines:list[str]):
    return client.post("/invoices/parse",files={"file":("invoice.pdf",pdf(lines),"application/pdf")})

def test_consistent_financial_values():
    response=upload(LINES)
    assert response.status_code==200, response.text
    assert response.json()["total_amount"]=="1071.00"

def test_wrong_total():
    assert upload([line.replace("Total: 1071.00","Total: 1072.00") for line in LINES]).status_code==422

def test_wrong_item_math():
    assert upload([line.replace("900.00 | 900.00","900.00 | 900.00").replace("3 | 300.00 | 900.00","3 | 300.00 | 901.00") for line in LINES]).status_code==422

def test_invalid_date_order_and_currency():
    assert upload([line.replace("Due Date: 2026-11-09","Due Date: 2026-09-01") for line in LINES]).status_code==422
    assert upload([line.replace("Currency: EUR","Currency: USD") for line in LINES]).status_code==422
