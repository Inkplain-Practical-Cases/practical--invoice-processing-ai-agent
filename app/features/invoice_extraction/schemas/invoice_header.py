# Why: stable invoice contract separates extraction from later business validation.
from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field, ConfigDict
from app.features.invoice_extraction.schemas.invoice_line_item import InvoiceLineItem

class InvoiceHeader(BaseModel):
    model_config = ConfigDict(extra="forbid")
    vendor: str = Field(min_length=2)
    invoice_number: str = Field(min_length=1)
    invoice_date: date
    due_date: date
    currency: str = Field(min_length=3, max_length=3)
    subtotal: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    items: list[InvoiceLineItem] = Field(min_length=1)
