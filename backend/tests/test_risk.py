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

@pytest.fixture
def engine(baseline_data):
    return SimulationEngine(baseline_data)

def test_calculate_sensitivity(engine, baseline_data):
    analyzer = RiskAnalyzer()
    sensitivity = analyzer.calculate_sensitivity(engine, baseline_data)

    assert 'revenue' in sensitivity
    assert 'operational_costs' in sensitivity
    assert 'marketing_spend' in sensitivity

    # Revenue increase should increase cash flow
    assert sensitivity['revenue'] > 0

    # Cost increase should decrease cash flow
    assert sensitivity['operational_costs'] < 0

def test_prob_of_failure(engine):
    analyzer = RiskAnalyzer()
    # Mock monte carlo results
    mc_results = {
        'mean': 40000,
        'std_dev': 10000,
        'iterations': 1000
    }

    # Threshold 0.0 (Breakeven)
    # Mean is 40k, std dev is 10k. 0 is 4 sigmas away. Prob should be very low.
    prob = analyzer.prob_of_failure(mc_results, threshold=0.0)
    assert prob < 0.01

    # Threshold 40000 (Mean)
    # Prob should be 0.5
    prob = analyzer.prob_of_failure(mc_results, threshold=40000)
    assert 0.49 < prob < 0.51
