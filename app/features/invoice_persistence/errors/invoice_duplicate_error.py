# Why: a typed domain name for a repeated invoice, kept separate from SQL error text.
class InvoiceDuplicateError(ValueError):
    pass
