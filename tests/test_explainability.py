import pytest
from backend.engine.explainability import DriverAnalyzer, EvidenceTracer

def test_driver_ranking():
    # Mock sensitivity data: Revenue impact 20%, Costs impact 50%, Marketing 10%
    sensitivity = {"revenue": 0.20, "operational_costs": -0.50, "marketing_spend": -0.10}
    
    analyzer = DriverAnalyzer()
    drivers = analyzer.analyze_drivers(sensitivity)
    
    # Costs should be #1 (absolute impact 0.50)
    assert drivers[0]["name"] == "operational_costs"
    assert drivers[0]["impact_score"] == 0.50
    
    # Revenue #2
    assert drivers[1]["name"] == "revenue"

def test_bridge_chart_data():
    analyzer = DriverAnalyzer()
    
    baseline = 1000
    scenario = 1200 # +200 variance
    
    drivers = [
        {"name": "input_A", "impact_score": 0.8},
        {"name": "input_B", "impact_score": 0.2}
    ]
    
    # Total variance = 200.
    # A has 80% share -> 160
    # B has 20% share -> 40
    
    bridge = analyzer.generate_bridge_data(baseline, scenario, drivers)
    
    assert bridge["start"] == 1000
    assert bridge["end"] == 1200
    assert len(bridge["steps"]) == 2
    
    assert bridge["steps"][0]["category"] == "input_A"
    assert pytest.approx(bridge["steps"][0]["value"]) == 160.0

def test_evidence_tracing():
    tracer = EvidenceTracer()
    constraints = {"budget": 5000}
    
    citations = tracer.trace_constraints(constraints)
    
    assert len(citations) == 1
    assert "[Constraint:1] budget <= 5000" in citations[0]
