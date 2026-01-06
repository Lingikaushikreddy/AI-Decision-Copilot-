from typing import Dict, List, Any
import numpy as np

class DriverAnalyzer:
    def analyze_drivers(self, sensitivity_data: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Ranks inputs by their impact (sensitivity).
        Returns a sorted list of drivers with their impact score and direction.
        """
        drivers = []
        for input_name, impact in sensitivity_data.items():
            drivers.append({
                "name": input_name,
                "impact_score": abs(impact),
                "direction": "Positive" if impact > 0 else "Negative",
                "magnitude": f"{impact*100:.1f}%"
            })
        
        # Sort by absolute impact (descending)
        drivers.sort(key=lambda x: x["impact_score"], reverse=True)
        return drivers

    def analyze_segment_drivers(self, sensitivity_data: Dict[str, float], separator: str = "::") -> List[Dict[str, Any]]:
        """
        Aggregates drivers by segment (prefix) if keys are hierarchical.
        Example: 'North::Revenue' -> segment 'North'.
        """
        segments = {}
        for key, impact in sensitivity_data.items():
            if separator in key:
                seg = key.split(separator)[0]
                segments[seg] = segments.get(seg, 0) + abs(impact)
            else:
                # Treat non-segmented as their own segment
                segments[key] = segments.get(key, 0) + abs(impact)

        # Convert to list
        results = [{"name": k, "total_impact": v} for k,v in segments.items()]
        results.sort(key=lambda x: x["total_impact"], reverse=True)
        return results

    def generate_bridge_data(self, baseline_val: float, scenario_val: float, drivers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generates data for a 'Bridge Chart' (Waterfall).
        Simplified logic: Distributes the total variance (scenario - baseline) 
        proportionally among the top drivers based on their impact score.
        """
        total_variance = scenario_val - baseline_val
        bridge_steps = []
        
        remaining_variance = total_variance
        
        # Attribute variance to top 3 drivers
        top_drivers = drivers[:3]
        total_impact_score = sum(d["impact_score"] for d in top_drivers)
        
        if total_impact_score == 0:
             return {"steps": []}

        for driver in top_drivers:
            # Proportion of the variance driven by this factor
            share = driver["impact_score"] / total_impact_score
            step_val = total_variance * share
            
            bridge_steps.append({
                "category": driver["name"],
                "value": step_val,
                "description": f"Impact from {driver['name']}"
            })
            remaining_variance -= step_val
            
        # Buckets rest into "Other"
        if abs(remaining_variance) > 0.01:
             bridge_steps.append({
                "category": "Other Factors",
                "value": remaining_variance,
                "description": "Cumulative impact of minor drivers"
            })
            
        return {
            "start": baseline_val,
            "end": scenario_val,
            "steps": bridge_steps
        }

class EvidenceTracer:
    def format_citation(self, source_type: str, source_id: str, content: str) -> str:
        """
        Formats a citation string for the UI.
        """
        return f"[{source_type}:{source_id}] {content}"

    def trace_constraints(self, active_constraints: Dict[str, float]) -> List[str]:
        """
        Returns citation strings for active constraints.
        """
        citations = []
        for i, (k, v) in enumerate(active_constraints.items()):
            citations.append(self.format_citation("Constraint", str(i+1), f"{k} <= {v}"))
        return citations
