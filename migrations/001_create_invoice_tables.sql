-- Educational PostgreSQL DDL; see provider models for the equivalent SQLAlchemy schema.
CREATE TABLE IF NOT EXISTS invoices (
 id SERIAL PRIMARY KEY,
 vendor VARCHAR(240) NOT NULL, invoice_number VARCHAR(120) NOT NULL,
 invoice_date DATE NOT NULL, due_date DATE NOT NULL, currency VARCHAR(3) NOT NULL,
 subtotal NUMERIC(12,2) NOT NULL, tax_amount NUMERIC(12,2) NOT NULL, total_amount NUMERIC(12,2) NOT NULL
);
CREATE TABLE IF NOT EXISTS invoice_line_items (
 id SERIAL PRIMARY KEY, invoice_id INTEGER NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
 description VARCHAR(240) NOT NULL, quantity NUMERIC(12,2) NOT NULL,
 unit_price NUMERIC(12,2) NOT NULL, line_total NUMERIC(12,2) NOT NULL
);
