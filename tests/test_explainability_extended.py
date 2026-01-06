import pytest
from backend.engine.explainability import NarrativeGenerator, MemoGenerator, DriverAnalyzer, EvidenceTracer

def test_narrative_recommendation():
    gen = NarrativeGenerator()
    drivers = [
        {"name": "revenue", "impact_score": 0.5, "direction": "Positive", "magnitude": "50.0%"},
        {"name": "costs", "impact_score": 0.3, "direction": "Negative", "magnitude": "30.0%"}
    ]
    rec = gen.generate_recommendation(drivers)
    assert "focus on revenue" in rec
    assert "highest impact (50.0%)" in rec
    assert "increase it" in rec

def test_narrative_risk():
    gen = NarrativeGenerator()
    risk_text = gen.generate_risk_assessment(0.6, ["revenue", "costs"])
    assert "Risk Level: Critical" in risk_text
    assert "60.0%" in risk_text
    assert "revenue, costs" in risk_text

def test_narrative_tradeoffs():
    gen = NarrativeGenerator()
    scenarios = {
        "Scenario A": {"cash_flow": 1000, "inputs": {"revenue": 100, "costs": 50}},
        "Scenario B": {"cash_flow": 800, "inputs": {"revenue": 90, "costs": 60}}
    }
    tradeoffs = gen.generate_tradeoffs(scenarios)
    assert len(tradeoffs) >= 2
    assert "yields $200 more cash flow" in tradeoffs[0]
    # Check if input differences are highlighted
    assert any("revenue" in t for t in tradeoffs)

def test_narrative_tradeoffs_custom_metric():
    gen = NarrativeGenerator()
    scenarios = {
        "Scenario A": {"roi": 0.20, "inputs": {}},
        "Scenario B": {"roi": 0.15, "inputs": {}}
    }
    tradeoffs = gen.generate_tradeoffs(scenarios, metric="roi")
    assert "yields $0 more roi" in tradeoffs[0] # Formatting assumes $ but metric name is used

def test_memo_generator():
    memo_gen = MemoGenerator()
    sim_results = {
        "mean": 5000,
        "p10": 1000,
        "p90": 9000,
        "prob_failure": 0.15
    }
    drivers = [
        {"name": "revenue", "impact_score": 0.5, "direction": "Positive", "magnitude": "50.0%"}
    ]
    scenarios = {
        "Base": {"cash_flow": 5000, "inputs": {}},
        "Growth": {"cash_flow": 6000, "inputs": {}}
    }
    sensitivity_data = {"North::Revenue": 0.5, "South::Revenue": 0.2}

    memo = memo_gen.create_memo(sim_results, drivers, scenarios, sensitivity_data)

    assert memo["title"] == "AI Decision Copilot: Executive Summary"
    assert memo["metrics"]["expected_outcome"] == 5000
    assert memo["narrative"]["risk_assessment"]
    assert "Moderate" in memo["narrative"]["risk_assessment"] # 0.15 is Moderate
    assert memo["metrics"]["target_metric"] == "cash_flow"

    # Check new fields
    assert "impact_tracing" in memo["evidence"]
    assert "segment_impacts" in memo["evidence"]
    # Check trace content
    assert any("North::Revenue" in s for s in memo["evidence"]["impact_tracing"])
    # Check segment aggregation
    assert memo["evidence"]["segment_impacts"][0]["name"] == "North"

def test_memo_generator_custom_metric():
    memo_gen = MemoGenerator()
    sim_results = {"mean": 100}
    drivers = [{"name": "input_A", "impact_score": 0.5, "direction": "Positive", "magnitude": "50%"}]

    memo = memo_gen.create_memo(sim_results, drivers, target_metric="roi")
    assert memo["metrics"]["target_metric"] == "roi"
    assert "roi" in memo["narrative"]["recommendation"]

def test_memo_generator_config():
    memo_gen = MemoGenerator()
    sim_results = {"mean": 100}
    drivers = []
    # Use custom separator and threshold
    sensitivity_data = {"North__Revenue": 0.05, "South__Revenue": 0.02}

    memo = memo_gen.create_memo(sim_results, drivers,
                                sensitivity_data=sensitivity_data,
                                tracing_threshold=0.03,
                                segment_separator="__")

    # North__Revenue (0.05) > 0.03 -> Should be traced
    # South__Revenue (0.02) < 0.03 -> Should NOT be traced
    assert len(memo["evidence"]["impact_tracing"]) == 1
    assert "North__Revenue" in memo["evidence"]["impact_tracing"][0]

    # Segment aggregation should work with __
    assert memo["evidence"]["segment_impacts"][0]["name"] == "North"

def test_trace_impact():
    tracer = EvidenceTracer()
    sensitivity = {"revenue": 0.2, "costs": 0.05}
    impacts = tracer.trace_impact(sensitivity, threshold=0.1)
    assert len(impacts) == 1
    assert "revenue" in impacts[0]
    assert "costs" not in impacts[0]

def test_segment_drivers():
    analyzer = DriverAnalyzer()
    sensitivity = {
        "North::Revenue": 0.1,
        "South::Revenue": 0.2,
        "Global::Costs": 0.05
    }
    segments = analyzer.analyze_segment_drivers(sensitivity)

    # Should have North, South, Global
    assert len(segments) == 3
    # Check order
    assert segments[0]["name"] == "South" # 0.2
    assert segments[1]["name"] == "North" # 0.1
    assert segments[2]["name"] == "Global" # 0.05
