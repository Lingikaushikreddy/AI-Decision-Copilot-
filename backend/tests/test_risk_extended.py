import pytest
from backend.engine.simulation import SimulationEngine
from backend.engine.risk import RiskAnalyzer

@pytest.fixture
def baseline_data():
    return {
        'revenue': 100000,
        'fixed_costs': 20000,
        'operational_costs': 30000,
        'marketing_spend': 10000
    }
# Cash Flow = 100k - (20k + 30k + 10k) = 40k

@pytest.fixture
def engine(baseline_data):
    return SimulationEngine(baseline_data)

@pytest.fixture
def analyzer():
    return RiskAnalyzer()

def test_calculate_breakpoints(engine, baseline_data, analyzer):
    # Current cash flow = 40k.
    # To hit 0 cash flow (threshold=0), revenue needs to drop by 40k.
    # So break-even revenue should be 60k.
    breakpoints = analyzer.calculate_breakpoints(engine, baseline_data, threshold=0.0)

    assert 'revenue' in breakpoints
    assert pytest.approx(breakpoints['revenue'], 1.0) == 60000

    # Operational costs need to increase by 40k.
    # So break-even op costs should be 30k + 40k = 70k.
    assert pytest.approx(breakpoints['operational_costs'], 1.0) == 70000

def test_run_stress_test(engine, baseline_data, analyzer):
    results = analyzer.run_stress_test(engine, baseline_data)

    assert "Recession" in results
    assert "Inflation" in results

    # Recession: Revenue * 0.8 = 80k. Cash flow = 80k - 60k = 20k.
    assert results["Recession"]["cash_flow"] == 20000

    # Inflation: Op Costs * 1.15 = 30k * 1.15 = 34.5k.
    # Cash flow = 100k - (20k + 34.5k + 10k) = 100k - 64.5k = 35.5k.
    assert results["Inflation"]["cash_flow"] == 35500
