import logging
import json
from datetime import datetime
import re

class AuditLogger:
    def __init__(self):
        self.logger = logging.getLogger("audit_logger")
        handler = logging.FileHandler("audit_trail.jsonl")
        handler.setFormatter(logging.Formatter('%(message)s'))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

        # Keys that often contain sensitive info
        # We will check if these substrings exist in the key (case-insensitive)
        self.sensitive_substrings = {'password', 'token', 'secret', 'key', 'auth', 'ssn', 'credit_card', 'pin'}

    def _redact_data(self, data):
        """
        Recursively redact sensitive keys in a dictionary or list.
        """
        if isinstance(data, dict):
            new_data = {}
            for k, v in data.items():
                # Check for sensitive substring in key
                if any(s in k.lower() for s in self.sensitive_substrings):
                    new_data[k] = "***REDACTED***"
                else:
                    new_data[k] = self._redact_data(v)
            return new_data
        elif isinstance(data, list):
            return [self._redact_data(item) for item in data]
        else:
            return data

    def log_event(self, user_id: str, action: str, details: dict):
        # Redact sensitive info from details before logging
        safe_details = self._redact_data(details)

        event = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "action": action,
            "details": safe_details
        }
        self.logger.info(json.dumps(event))

# Singleton instance
audit_logger = AuditLogger()
