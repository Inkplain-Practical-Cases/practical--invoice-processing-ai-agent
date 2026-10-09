# Why: logs must be structured and exclude raw PDF contents, vendor names and tokens.
import json
import logging
logger = logging.getLogger("northstar.invoice")

def service_log_invoice_event(event: str, invoice_id: int | None, result: str) -> None:
    logger.info(json.dumps({"event":event,"invoice_id":invoice_id,"result":result},sort_keys=True))
