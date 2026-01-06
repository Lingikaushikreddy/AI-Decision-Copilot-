import pytest
from fastapi.testclient import TestClient
from backend.main import app
import os
import shutil

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def temp_audit_file():
    # Setup: Use a temp file for audit logs to avoid cluttering the repo
    # Note: The AuditLogger is a singleton instantiated at import time.
    # To properly mock it, we might need to patch it or handle the file cleanup.
    # For integration tests, we'll let it write to the default file and clean up.
    yield "audit_trail.jsonl"
    # Teardown
    if os.path.exists("audit_trail.jsonl"):
        os.remove("audit_trail.jsonl")

@pytest.fixture
def sample_csv_content():
    return b"date,category,amount\n2023-01-01,Sales,100\n2023-01-02,Sales,200"

@pytest.fixture
def bad_csv_content():
    return b"Not a CSV file\nJust some random text"

@pytest.fixture
def anomaly_csv_content():
    return b"date,category,amount\n2023-01-01,Sales,-100\n2023-01-02,Sales,200"
