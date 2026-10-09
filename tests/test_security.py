# Why: test that audit logs avoid invoice text, vendor names and auth material.
import json,logging
from app.core.observability import service_log_invoice_event

def test_safe_json_event(caplog):
    with caplog.at_level(logging.INFO,logger="northstar.invoice"):
        service_log_invoice_event("invoice_stored",42,"success")
    message=caplog.records[-1].message
    assert json.loads(message)=={"event":"invoice_stored","invoice_id":42,"result":"success"}
    assert "token" not in message.lower()
    assert "vendor" not in message.lower()
