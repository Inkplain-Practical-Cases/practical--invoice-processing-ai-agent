# Why: PostgreSQL must reject duplicate normalized vendor/invoice keys.
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from sqlalchemy import func, select
from app.main import app
from app.providers.database.models import InvoiceORM
from app.providers.database.session import get_db_session
client=TestClient(app)

def invoice_pdf(vendor="Northstar Supplies")->bytes:
    lines=[f"Vendor: {vendor}","Invoice No: INV-2026-0042",
           "Invoice Date: 2026-10-09","Due Date: 2026-11-09","Currency: EUR",
           "Item: Monitor | 3 | 300.00 | 900.00","Subtotal: 900.00",
           "Tax: 171.00","Total: 1071.00"]
    b=BytesIO()
    c=canvas.Canvas(b)
    for i,line in enumerate(lines): c.drawString(35,760-24*i,line)
    c.save()
    return b.getvalue()

def send(data:bytes):
    return client.post("/invoices/process",files={"file":("invoice.pdf",data,"application/pdf")})

def test_duplicate_vendor_invoice_is_http_409():
    assert send(invoice_pdf()).status_code==201
    response=send(invoice_pdf("  NORTHSTAR   SUPPLIES  "))
    assert response.status_code==409, response.text
    with get_db_session() as db:
        assert db.scalar(select(func.count()).select_from(InvoiceORM))==1

def test_concurrent_duplicate_only_one_inserts():
    payload=invoice_pdf()
    with ThreadPoolExecutor(max_workers=2) as executor:
        responses=list(executor.map(send,[payload,payload]))
    assert sorted(x.status_code for x in responses)==[201,409]
    with get_db_session() as db:
        assert db.scalar(select(func.count()).select_from(InvoiceORM))==1
