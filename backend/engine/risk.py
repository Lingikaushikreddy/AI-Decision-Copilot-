from typing import Dict, List
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
