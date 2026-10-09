# Why: durable invoice headers and line items belong to one transactional database.
from datetime import date
from decimal import Decimal
from sqlalchemy import Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class InvoiceORM(Base):
    __tablename__ = "invoices"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    vendor: Mapped[str] = mapped_column(String(240), nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(120), nullable=False)
    invoice_date: Mapped[date] = mapped_column(Date, nullable=False)
    due_date: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    items: Mapped[list["InvoiceLineItemORM"]] = relationship(back_populates="invoice", cascade="all, delete-orphan")

class InvoiceLineItemORM(Base):
    __tablename__ = "invoice_line_items"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id", ondelete="CASCADE"), nullable=False)
    description: Mapped[str] = mapped_column(String(240), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    line_total: Mapped[Decimal] = mapped_column(Numeric(12,2), nullable=False)
    invoice: Mapped[InvoiceORM] = relationship(back_populates="items")
