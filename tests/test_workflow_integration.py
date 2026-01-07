import pytest
import os
import json

def test_simulation_workflow(client):
    payload = {
        "marketing_spend_delta": 1000.0,
        "hiring_freeze": True
    }
    response = client.post("/api/workflow/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "baseline_cash" in data
    assert "scenario_cash" in data
    assert "savings_impact" in data
    # Check that savings impact is positive (due to hiring freeze)
    # Hiring freeze saves 2000, Marketing spend costs 1000 -> Net savings should be ~1000 positive?
    # Wait, savings_impact calculation:
    # mc_results['mean'] - (baseline['revenue'] - sum(list(baseline.values())[1:]))
    # Baseline costs: 15k + 20k + 5k = 40k. Rev 50k. Net 10k.
    # Scenario costs: 15k + 18k + 6k = 39k. Rev 50k. Net 11k.
    # Impact should be ~1000.
    # Note: MC results vary, but mean should be close.
    assert data["savings_impact"] > 500  # allowing some variance/margin

def test_memo_generation(client):
    payload = {
        "scenario_id": "123",
        "decision_type": "Hiring Freeze"
    }
    response = client.post("/api/workflow/memo", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MEMO-123"
    assert "Hiring Freeze" in data["title"]

def test_audit_log_creation(client, temp_audit_file):
    # Trigger an action
    payload = {
        "marketing_spend_delta": 500.0,
        "hiring_freeze": False
    }
    client.post("/api/workflow/simulate", json=payload)

    # Check if audit file exists and has content
    assert os.path.exists("audit_trail.jsonl")
    with open("audit_trail.jsonl", "r") as f:
        lines = f.readlines()
        assert len(lines) > 0
        last_entry = json.loads(lines[-1])
        # The middleware logs the request
        assert "AUDIT: POST" in last_entry or "action" in last_entry
