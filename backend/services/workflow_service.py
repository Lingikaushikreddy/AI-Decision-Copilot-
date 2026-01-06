from backend.engine.simulation import SimulationEngine
from backend.engine.risk import RiskAnalyzer

class WorkflowService:
    def run_simulation(self, params):
        # Param mapping (simplified)
        baseline = {
            "revenue": 50000.0,
            "fixed_costs": 15000.0,
            "operational_costs": 20000.0,
            "marketing_spend": 5000.0
        }
        
        # Apply overrides from params
        overrides = {}
        if params.hiring_freeze:
             overrides["operational_costs"] = 18000.0 # Save 2k
             
        if params.marketing_spend_delta != 0:
             overrides["marketing_spend"] = baseline["marketing_spend"] + params.marketing_spend_delta

        # Run Engine
        engine = SimulationEngine(baseline)
        mc_results = engine.run_monte_carlo(overrides, iterations=1000)
        
        # Calculate Mock Cash Flow Series for Chart (P50 trend)
        # In a real app, we'd simulate time-series month-over-month.
        # Here we just distribute the annual result roughly over 6 months
        monthly_avg = mc_results['p50'] / 6
        scenario_trend = [monthly_avg * (1 + i*0.05) for i in range(6)] # grow slightly
        
        return {
            "baseline_cash": [5000] * 6, # flat baseline
            "scenario_cash": scenario_trend,
            "savings_impact": mc_results['mean'] - (baseline['revenue'] - sum(list(baseline.values())[1:])),
            "uncertainty": {
                "p10": mc_results['p10'],
                "p90": mc_results['p90'],
                "std_dev": mc_results['std_dev']
            }
        }

    def generate_memo(self, scenario_id: str, decision_type: str):
        # In real app, would use LLM to generate text based on scenario data
        return {
            "id": f"MEMO-{scenario_id}",
            "title": f"Recommendation: {decision_type}",
            "confidence_score": "High (85%)",
            "bluf": "Based on the simulation, implementing this decision yields a positive ROI of 15% whilst preserving core operational capacity.",
            "trade_offs": ["Increased support wait times", "Slower regional expansion"],
            "generated_at": "2024-10-24T14:30:00Z"
        }
