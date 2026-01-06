from typing import Dict, List, Any
import numpy as np

class RiskAnalyzer:
    def calculate_sensitivity(self, engine, base_inputs: Dict[str, float], metric: str = 'cash_flow') -> Dict[str, float]:
        """
        One-At-A-Time (OAT) Sensitivity Analysis.
        Perturbs each input by +10% to measure impact on output metric.
        Returns % change in output.
        """
        baseline_res = engine.run_deterministic(base_inputs)
        base_val = baseline_res[metric]
        
        sensitivity = {}
        for key in ['revenue', 'operational_costs', 'marketing_spend']:
            if key not in base_inputs: continue
            
            # Perturb +10%
            new_inputs = base_inputs.copy()
            new_inputs[key] *= 1.10
            
            new_res = engine.run_deterministic(new_inputs)
            new_val = new_res[metric]
            
            sensitivity[key] = (new_val - base_val) / base_val
            
        return sensitivity

    def calculate_breakpoints(self, engine, base_inputs: Dict[str, float], threshold: float = 0.0) -> Dict[str, float]:
        """
        Calculates at what value of each input the output metric crosses the threshold (break-even).
        Assumes linear relationship for simplicity (or uses Newton-Raphson if complex, but here linear is fine).
        """
        baseline_res = engine.run_deterministic(base_inputs)
        base_val = baseline_res['cash_flow']

        breakpoints = {}
        for key in ['revenue', 'operational_costs', 'marketing_spend']:
            if key not in base_inputs: continue

            # Simple linear extrapolation: y = mx + c
            # We have point 1: (x1, y1) = (base_input, base_val)
            # We need to find x where y = threshold.

            # Let's find slope 'm' by perturbing.
            x1 = base_inputs[key]
            y1 = base_val

            # Perturb +1% for slope calculation
            delta_x = x1 * 0.01 if x1 != 0 else 1.0
            new_inputs = base_inputs.copy()
            new_inputs[key] = x1 + delta_x

            new_res = engine.run_deterministic(new_inputs)
            y2 = new_res['cash_flow']

            slope = (y2 - y1) / delta_x

            if slope == 0:
                breakpoints[key] = float('inf') # No impact
            else:
                # y - y1 = m(x - x1)
                # threshold - y1 = m(x - x1)
                # (threshold - y1)/m = x - x1
                # x = x1 + (threshold - y1)/m
                x_break = x1 + (threshold - y1) / slope
                breakpoints[key] = x_break

        return breakpoints

    def run_stress_test(self, engine, base_inputs: Dict[str, float]) -> Dict[str, Any]:
        """
        Runs predefined stress scenarios (e.g., 'Recession', 'Supply Shock').
        """
        scenarios = {
            "Recession": {"revenue": 0.8}, # -20% Revenue
            "Inflation": {"operational_costs": 1.15}, # +15% Costs
            "Aggressive Growth": {"marketing_spend": 1.5, "revenue": 1.2} # +50% Spend, +20% Revenue
        }

        results = {}
        for name, modifiers in scenarios.items():
            # Apply modifiers
            scenario_inputs = base_inputs.copy()
            for key, multiplier in modifiers.items():
                if key in scenario_inputs:
                    scenario_inputs[key] *= multiplier

            res = engine.run_deterministic(scenario_inputs)
            results[name] = {
                "inputs": scenario_inputs,
                "cash_flow": res["cash_flow"]
            }
        return results

    def prob_of_failure(self, monte_carlo_results: Dict[str, Any], threshold: float = 0.0) -> float:
        """
        Calculates probability (0.0-1.0) that the metric falls below a threshold (e.g., negative cash flow).
        Note: This requires access to the full distribution array, which we simplified in the engine response.
        For now, we approximate using normal distribution properties (Z-score) since we have mean/std.
        """
        if monte_carlo_results['std_dev'] == 0: return 0.0
        
        import scipy.stats as stats
        z_score = (threshold - monte_carlo_results['mean']) / monte_carlo_results['std_dev']
        prob = stats.norm.cdf(z_score)
        return float(prob)
