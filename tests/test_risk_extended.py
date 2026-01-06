import pytest
from backend.engine.simulation import SimulationEngine
from backend.engine.risk import RiskAnalyzer

def test_breakpoints_revenue_drop():
    # Baseline: Rev=100, Costs=30. Cash=70.
    # Breakpoint for Cash=0 should be Rev=30.
    baseline = {"revenue": 100, "fixed_costs": 10, "operational_costs": 10, "marketing_spend": 10}
    engine = SimulationEngine(baseline)
    risk = RiskAnalyzer()
    
    breakpoints = risk.calculate_breakpoints(engine, baseline, threshold=0)
    
    # Revenue needs to drop TO 30 to reach 0 cash flow.
    assert pytest.approx(breakpoints['revenue'], 1.0) == 30.0

def test_stress_test_execution():
    baseline = {"revenue": 1000, "fixed_costs": 200, "operational_costs": 300, "marketing_spend": 100}
    engine = SimulationEngine(baseline)
    risk = RiskAnalyzer()
    
    results = risk.run_stress_test(engine, baseline)
    
    # Recession: Rev * 0.8 = 800. Costs=600. Cash=200.
    assert "Recession" in results
    assert results["Recession"]["cash_flow"] == 200.0
    
    # Inflation: OpCosts * 1.15 = 345. Total Costs = 200+345+100 = 645. Rev=1000. Cash=355.
    assert "Inflation" in results
    assert results["Inflation"]["cash_flow"] == 355.0

def test_constraint_enforcement():
    baseline = {"revenue": 100, "fixed_costs": 0, "operational_costs": 0, "marketing_spend": 100}
    engine = SimulationEngine(baseline)
    
    # Try to spend 200, but clamp at 150
    constraints = {"marketing_spend": 150}
    overrides = {"marketing_spend": 200}
    
    res = engine.run_deterministic(overrides=overrides, constraints=constraints)
    
    # Spend should be clamped to 150
    # Cash = 100 - 150 = -50
    assert res['inputs']['marketing_spend'] == 150
    assert res['cash_flow'] == -50
