import pandas as pd
import numpy as np
from typing import List, Dict, Any

class ETLPipeline:
    def _calculate_confidence_scores(self, decision_table: pd.DataFrame) -> pd.Series:
        """
        Calculates per-row confidence scores using IQR-based outlier detection.
        Normal values get 0.95, mild outliers get 0.70, extreme outliers get 0.50.
        """
        scores = pd.Series(0.95, index=decision_table.index)

        for metric_name, group in decision_table.groupby('metric_name'):
            values = group['metric_value']
            if len(values) < 4:
                # Too few data points for meaningful IQR — keep default
                continue

            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            if iqr == 0:
                # IQR is zero (majority of values are identical).
                # Fall back to standard-deviation-based detection for the remaining spread.
                std = values.std()
                if std == 0:
                    continue  # truly all identical
                mean = values.mean()
                extreme_mask = (np.abs(values - mean) > 3 * std)
                mild_mask = (np.abs(values - mean) > 2 * std) & ~extreme_mask
                scores.loc[group.index[mild_mask]] = 0.70
                scores.loc[group.index[extreme_mask]] = 0.50
                continue

            lower_fence = q1 - 1.5 * iqr
            upper_fence = q3 + 1.5 * iqr
            extreme_lower = q1 - 3.0 * iqr
            extreme_upper = q3 + 3.0 * iqr

            extreme_mask = (values < extreme_lower) | (values > extreme_upper)
            mild_mask = ((values < lower_fence) | (values > upper_fence)) & ~extreme_mask

            scores.loc[group.index[mild_mask]] = 0.70
            scores.loc[group.index[extreme_mask]] = 0.50

        return scores

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
        # Lower confidence for outliers detected via IQR method
        decision_table['confidence_score'] = self._calculate_confidence_scores(decision_table)

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
