-- For upgrading STEP-4 PostgreSQL schemas. Existing duplicates must be resolved first.
ALTER TABLE invoices ADD COLUMN IF NOT EXISTS vendor_normalized VARCHAR(240);
UPDATE invoices SET vendor_normalized=LOWER(REGEXP_REPLACE(TRIM(vendor), '[[:space:]]+', ' ', 'g'))
WHERE vendor_normalized IS NULL;
ALTER TABLE invoices ALTER COLUMN vendor_normalized SET NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS uq_vendor_invoice ON invoices(vendor_normalized,invoice_number);
