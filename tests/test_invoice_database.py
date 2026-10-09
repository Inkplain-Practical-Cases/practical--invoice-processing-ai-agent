# Why: test that real HTTP → SQLAlchemy → database persists invoice and child rows together.
from io import BytesIO
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from sqlalchemy import select, func
from app.main import app
from app.providers.database.models import InvoiceLineItemORM
from app.providers.database.session import get_db_session

client=TestClient(app)
LINES=["Vendor: Northstar Supplies","Invoice No: INV-2026-0042",
       "Invoice Date: 2026-10-09","Due Date: 2026-11-09","Currency: EUR",
       "Item: Monitor | 3 | 300.00 | 900.00","Subtotal: 900.00","Tax: 171.00","Total: 1071.00"]

def sample_pdf()->bytes:
    stream=BytesIO()
    c=canvas.Canvas(stream)
    for i,line in enumerate(LINES):
        c.drawString(35,760-24*i,line)
    c.save()
    return stream.getvalue()

def test_insert_and_fetch():
    result=client.post("/invoices/process",files={"file":("invoice.pdf",sample_pdf(),"application/pdf")})
    assert result.status_code==201, result.text
    identifier=result.json()["id"]
    fetched=client.get(f"/invoices/{identifier}")
    assert fetched.status_code==200
    assert fetched.json()["invoice_number"]=="INV-2026-0042"
    with get_db_session() as session:
        count=session.scalar(select(func.count()).select_from(InvoiceLineItemORM))
    assert count==1

def test_missing_invoice_returns_404():
    assert client.get("/invoices/999999").status_code==404
