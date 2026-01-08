import pandas as pd
from typing import List, Dict, Any

class ETLPipeline:
    def standardize_to_decision_table(self, df: pd.DataFrame, 
                                      entity_col: str, 
                                      time_col: str) -> pd.DataFrame:
        """
        Transforms a wide DataFrame into a standardized long-format Decision Table.
        Format: [entity_id, time, metric_name, metric_value, confidence_score]
        """
        
        # Basic validation
        if entity_col not in df.columns or time_col not in df.columns:
            raise ValueError(f"Columns {entity_col} or {time_col} not found in dataset")
            
        # Ensure time is datetime
        df[time_col] = pd.to_datetime(df[time_col])
        
        # Identify metric columns (assume numeric for now)
        metric_cols = df.select_dtypes(include=['number']).columns.tolist()
        if entity_col in metric_cols: metric_cols.remove(entity_col)
        
        # Melt to long format
        decision_table = df.melt(
            id_vars=[entity_col, time_col],
            value_vars=metric_cols,
            var_name='metric_name',
            value_name='metric_value'
        )
        
        # specific normalization (e.g. handle nulls in metrics)
        decision_table = decision_table.dropna(subset=['metric_value'])
        
        # Generate Confidence Score per row
        # Logic: Lower confidence for outliers or imputed values (mock logic)
        decision_table['confidence_score'] = 0.95 
        
        return decision_table

    def generate_confidence_report(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Returns field-level confidence stats.
        """
        report = {}
        for col in df.columns:
            null_count = df[col].isnull().sum()
            total_count = len(df)
            
            score = 1.0 - (null_count / total_count)
            report[col] = {
                "completeness": round(score, 2),
                "warnings": []
            }
            if score < 0.8:
                report[col]["warnings"].append("Low data completeness")
                
        return report

    def validate_schema(self, df: pd.DataFrame, required_columns: List[str] = ["Revenue", "Costs"]) -> Dict[str, Any]:
        """
        Validates that the dataframe contains necessary columns for simulation.
        """
        missing = [col for col in required_columns if col not in df.columns]
        
        return {
            "is_valid": len(missing) == 0,
            "missing_columns": missing
        }
