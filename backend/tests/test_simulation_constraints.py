import pytest
from backend.engine.simulation import SimulationEngine

@pytest.fixture
def baseline_data():
    return {
        'revenue': 100000,
        'fixed_costs': 20000,
        'operational_costs': 30000,
        'marketing_spend': 10000
    }

def test_constraints_deterministic(baseline_data):
    engine = SimulationEngine(baseline_data)

    # Try to set marketing_spend to 50k, but constrain to 20k
    constraints = {'marketing_spend': 20000}
    overrides = {'marketing_spend': 50000}

    result = engine.run_deterministic(overrides, constraints)

    assert result['inputs']['marketing_spend'] == 20000
    # Cash flow = 100k - (20k + 30k + 20k) = 30k
    assert result['cash_flow'] == 30000

def test_constraints_monte_carlo(baseline_data):
    engine = SimulationEngine(baseline_data)
    constraints = {'marketing_spend': 20000}
    overrides = {'marketing_spend': 50000}

    result = engine.run_monte_carlo(overrides, constraints, iterations=100)

    # Since marketing_spend is part of the fixed inputs (not perturbed in this simple model),
    # it should be respected in the mean calculation logic implicitly because base_inputs are derived from run_deterministic.

    # We don't have direct access to the inputs used in MC result object, but we can check the mean.
    # Mean should approximate deterministic run with constraint.
    # Expected mean ~ 30000

    # Standard deviation of cash flow comes from Revenue (5k) and Op Costs (900).
    # Sqrt(5000^2 + 900^2) approx 5080.

    assert 28000 < result['mean'] < 32000
