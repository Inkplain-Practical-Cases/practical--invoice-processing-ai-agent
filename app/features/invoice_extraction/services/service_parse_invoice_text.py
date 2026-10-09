# Why: parse known synthetic invoice lines deterministically, never invent missing fields.
from fastapi import HTTPException
from pydantic import ValidationError
from app.features.invoice_extraction.schemas.invoice_header import InvoiceHeader

FIELDS = {
    "Vendor": "vendor", "Invoice No": "invoice_number", "Invoice Date": "invoice_date",
    "Due Date": "due_date", "Currency": "currency", "Subtotal": "subtotal",
    "Tax": "tax_amount", "Total": "total_amount",
}

def service_parse_invoice_text(text: str) -> InvoiceHeader:
    values: dict = {"items": []}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("Item:"):
            # Teaching format: Item: description | quantity | unit price | line total
            parts = [s.strip() for s in line[5:].split("|")]
            if len(parts) != 4:
                raise HTTPException(status_code=422, detail="Malformed invoice item")
            values["items"].append(dict(zip(("description","quantity","unit_price","line_total"),parts)))
            continue
        if ":" in line:
            label, value = line.split(":", 1)
            if label.strip() in FIELDS:
                values[FIELDS[label.strip()]] = value.strip()
    try:
        return InvoiceHeader.model_validate(values)
    except ValidationError as exc:
        # Expose field names, not full vendor document or raw exceptions.
        names = sorted({str(e["loc"][0]) for e in exc.errors()})
        raise HTTPException(status_code=422, detail={"invalid_fields": names}) from exc
