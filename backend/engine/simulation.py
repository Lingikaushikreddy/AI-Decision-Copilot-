import numpy as np
from typing import Dict, List, Any

class SimulationEngine:
    def __init__(self, baseline_data: Dict[str, float]):
        """
        baseline_data: Dictionary containing 'revenue', 'fixed_costs', 'operational_costs', 'marketing_spend'
        """
        self.baseline = baseline_data

    def _calculate_cash_flow(self, data: Dict[str, float]) -> float:
        """Deterministic Cash Flow Calculation"""
        return data['revenue'] - (data['fixed_costs'] + data['operational_costs'] + data['marketing_spend'])

    def run_deterministic(self, overrides: Dict[str, float] = None, constraints: Dict[str, float] = None) -> Dict[str, float]:
        """
        Runs a single deterministic simulation with optional overrides.
        constraints: Optional dict of maximum allowed values (e.g., {'marketing_spend': 50000})
        """
        data = self.baseline.copy()
        if overrides:
            data.update(overrides)
        
        # Apply constraints
        if constraints:
            for key, max_val in constraints.items():
                if key in data and data[key] > max_val:
                    # Depending on policy, we could raise error or clamp.
                    # Given it's a "what-if" tool, clamping and notifying might be better,
                    # but for now, let's clamp silently or we can return a warning flag.
                    data[key] = max_val

        cash_flow = self._calculate_cash_flow(data)
        return {"cash_flow": cash_flow, "inputs": data}

    def run_monte_carlo(self, overrides: Dict[str, float] = None, constraints: Dict[str, float] = None, iterations: int = 1000) -> Dict[str, Any]:
        """
        Runs Monte Carlo simulation.
        Perturbs 'revenue' by +/- 10% and 'costs' by +/- 5% (simulating uncertainty).
        """
        base_run = self.run_deterministic(overrides, constraints)
        base_inputs = base_run["inputs"]
        
        # Vectorized perturbation
        # Random normal distribution for Revenue (std dev = 5% of mean)
        rev_dist = np.random.normal(base_inputs['revenue'], base_inputs['revenue'] * 0.05, iterations)
        
        # Random normal for Var Costs (std dev = 3% of mean)
        op_cost_dist = np.random.normal(base_inputs['operational_costs'], base_inputs['operational_costs'] * 0.03, iterations)
        
        # Apply constraints to distributions if needed (e.g. costs cannot exceed constraint even with perturbation)
        # For simplicity, we assume constraints apply to the BASE DECISION, not the stochastic outcome of external factors.
        # However, if 'marketing_spend' was perturbed, we would clamp it. But here it's fixed in the base inputs.

        # Calculate distribution of outcomes
        cash_flow_dist = rev_dist - (base_inputs['fixed_costs'] + op_cost_dist + base_inputs['marketing_spend'])
        
        return {
            "p10": np.percentile(cash_flow_dist, 10),
            "p50": np.percentile(cash_flow_dist, 50),
            "p90": np.percentile(cash_flow_dist, 90),
            "mean": np.mean(cash_flow_dist),
            "std_dev": np.std(cash_flow_dist),
            "iterations": iterations
        }
