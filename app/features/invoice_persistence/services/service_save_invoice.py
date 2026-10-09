# Why: storage service hides transactional repository details from HTTP handlers.
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader
from app.providers.database.session import get_db_session
from app.providers.database.invoice_repository import save_invoice

def service_save_invoice(invoice:InvoiceHeader)->dict:
    with get_db_session() as session:
        return save_invoice(session,invoice)
