# Why: make item quantity and unit price machine-readable and inspectable.
from decimal import Decimal
from pydantic import BaseModel, Field

class InvoiceLineItem(BaseModel):
    description: str = Field(min_length=1, max_length=240)
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(ge=0)
    line_total: Decimal = Field(ge=0)
