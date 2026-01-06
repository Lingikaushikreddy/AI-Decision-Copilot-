import pytest
from backend.engine.simulation import SimulationEngine
import numpy as np

def test_deterministic_calculation():
    baseline = {"revenue": 100, "fixed_costs": 10, "operational_costs": 10, "marketing_spend": 10}
    engine = SimulationEngine(baseline)
    
    result = engine.run_deterministic()
    assert result["cash_flow"] == 70.0 # 100 - 30

def test_monte_carlo_convergence():
    baseline = {"revenue": 10000, "fixed_costs": 1000, "operational_costs": 1000, "marketing_spend": 1000}
    engine = SimulationEngine(baseline)
    
    result = engine.run_monte_carlo(iterations=5000)
    
    # Mean of MC should be close to deterministic value (7000)
    # The perturbations are normal centered on the mean, so expected value is mean.
    det_val = 7000.0
    assert np.isclose(result["mean"], det_val, rtol=0.05) # within 5%
    assert result["p90"] > result["p10"]
