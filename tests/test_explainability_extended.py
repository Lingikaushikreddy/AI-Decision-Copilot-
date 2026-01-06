import pytest
from backend.engine.explainability import NarrativeGenerator, MemoGenerator, DriverAnalyzer

def test_narrative_generation():
    gen = NarrativeGenerator()
    
    # Test Recommendation
    drivers = [
        {"name": "Marketing Spend", "direction": "Positive", "magnitude": "40.0%"}
    ]
    rec = gen.generate_recommendation(drivers, metric="profit")
    assert "focus on Marketing Spend" in rec
    assert "increase" in rec # Positive direction
    
    # Test Risk Assessment
    risk_text = gen.generate_risk_assessment(prob_failure=0.6, sensitive_params=["Revenue"])
    assert "Risk Level: Critical" in risk_text
    assert "Revenue" in risk_text
    
    # Test Trade-offs
    scenarios = {
        "Scenario A": {"cash_flow": 100, "inputs": {"spend": 10}},
        "Scenario B": {"cash_flow": 80,  "inputs": {"spend": 5}}
    }
    tradeoffs = gen.generate_tradeoffs(scenarios, metric="cash_flow")
    assert len(tradeoffs) >= 2
    assert "$20 more cash flow" in tradeoffs[0]
    assert "requires spend to be 10" in tradeoffs[1]

def test_segment_analysis():
    analyzer = DriverAnalyzer()
    
    sensitivity = {
        "North::Revenue": 0.5,
        "South::Revenue": 0.2,
        "North::Costs": 0.1
    }
    
    segments = analyzer.analyze_segment_drivers(sensitivity)
    
    # North total = 0.5 + 0.1 = 0.6
    # South total = 0.2
    
    assert segments[0]["name"] == "North"
    assert segments[0]["total_impact"] == 0.6
    assert segments[1]["name"] == "South"

def test_memo_generator_structure():
    memo_gen = MemoGenerator()
    
    simulation_results = {"mean": 1000, "prob_failure": 0.1}
    driver_analysis = [{"name": "Driver A", "direction": "Positive", "magnitude": "10%"}]
    sensitivity_data = {"Driver A": 0.5}
    
    memo = memo_gen.create_memo(
        simulation_results=simulation_results,
        driver_analysis=driver_analysis,
        sensitivity_data=sensitivity_data
    )
    
    assert "metrics" in memo
    assert "narrative" in memo
    assert "evidence" in memo
    assert "impact_tracing" in memo["evidence"]
