import pytest
import numpy as np
from backend.engine.simulation import SimulationEngine

@pytest.fixture
def baseline_data():
    return {
        'revenue': 100000,
        'fixed_costs': 20000,
        'operational_costs': 30000,
        'marketing_spend': 10000
    }

def test_run_deterministic(baseline_data):
    engine = SimulationEngine(baseline_data)
    result = engine.run_deterministic()
    expected_cash_flow = 100000 - (20000 + 30000 + 10000)
    assert result['cash_flow'] == expected_cash_flow
    assert result['inputs'] == baseline_data

def test_run_deterministic_with_overrides(baseline_data):
    engine = SimulationEngine(baseline_data)
    overrides = {'revenue': 120000, 'marketing_spend': 15000}
    result = engine.run_deterministic(overrides)
    expected_cash_flow = 120000 - (20000 + 30000 + 15000)
    assert result['cash_flow'] == expected_cash_flow
    assert result['inputs']['revenue'] == 120000

def test_run_monte_carlo(baseline_data):
    engine = SimulationEngine(baseline_data)
    result = engine.run_monte_carlo(iterations=100)
    assert 'mean' in result
    assert 'p10' in result
    assert 'p50' in result
    assert 'p90' in result
    assert result['iterations'] == 100

    # Check that there is some variance (std_dev > 0)
    assert result['std_dev'] > 0
