# Why: identity normalization must be consistent before enforcing a database unique key.
def service_normalize_vendor(name: str) -> str:
    # Whitespace and case normalization are sufficient for synthetic examples.
    return " ".join(name.split()).casefold()
