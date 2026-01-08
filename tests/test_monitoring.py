import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.monitoring import monitor

client = TestClient(app)

def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text

def test_request_tracking():
    # Make a request to trigger middleware
    client.get("/health")
    
    # Check metrics (getting raw text)
    response = client.get("/metrics")
    metrics_text = response.text
    
    # Check that the request was counted
    assert 'http_requests_total{endpoint="/health",method="GET",status="200"}' in metrics_text

def test_token_tracking():
    # Simulate manual tracking
    monitor.track_tokens(100, model="gpt-4")
    
    response = client.get("/metrics")
    assert 'llm_token_usage_total{model="gpt-4",type="total"} 100.0' in response.text
