import pytest
import pandas as pd
from backend.services.security import PIIScrubber, LogSanitizer
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# --- 1. PII Scrubbing Tests ---
def test_pii_masking_email():
    scrubber = PIIScrubber()
    df = pd.DataFrame({
        "User": ["John Doe", "Jane Smith"],
        "Email": ["john.doe@example.com", "jane.smith@company.org"]
    })
    
    clean_df = scrubber.scrub_dataframe(df)
    
    # Check column content masking
    # Code sets it to [REDACTED_COL] if column name matches "Email"
    assert clean_df["Email"].iloc[0] == "[REDACTED_COL]"
    # Ensure original data is gone
    assert not clean_df["Email"].str.contains("@").any()

def test_pii_masking_ssn():
    scrubber = PIIScrubber()
    df = pd.DataFrame({
        "ID": [1, 2],
        "Notes": ["SSN is 123-45-6789", "No SSN here"]
    })
    
    clean_df = scrubber.scrub_dataframe(df)
    assert "123-45-6789" not in clean_df["Notes"][0]
    assert "[REDACTED_SSN_US]" in clean_df["Notes"][0]

# --- 2. Log Sanitization Tests ---
def test_log_sanitizer():
    sanitizer = LogSanitizer()
    dirty_log = {
        "user": "admin",
        "auth": "Bearer xyz123",
        "meta": {
            "api_key": "sk-123456",
            "timestamp": 12345
        }
    }
    
    clean_log = sanitizer.sanitize(dirty_log)
    
    assert clean_log["user"] == "admin"
    assert clean_log["auth"] == "***REDACTED***"
    assert clean_log["meta"]["api_key"] == "***REDACTED***"
    assert clean_log["meta"]["timestamp"] == 12345

# --- 3. Admin/Compliance API Tests ---
def test_data_deletion_endpoint():
    # Test valid deletion
    response = client.delete("/api/admin/data/user_123")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "user_123" in response.json()["message"]

def test_data_deletion_missing_id():
    response = client.delete("/api/admin/data/")
    assert response.status_code == 404 # Path not found because ID is required in path
