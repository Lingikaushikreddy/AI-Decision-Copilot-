import logging
import json
from datetime import datetime

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit_logger")
        handler = logging.FileHandler("audit_trail.jsonl")
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def log_event(self, user_id: str, action: str, details: dict):
        event = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": details
        }
        self.logger.info(json.dumps(event))

# Singleton instance
audit_logger = AuditLogger()
