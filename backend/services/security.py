import re
import pandas as pd
from typing import Dict, Any, List

class PIIScrubber:
    """
    Detects and masks Personally Identifiable Information (PII) in dataframes.
    """
    
    # Regex patterns for common PII
    PATTERNS = {
        "EMAIL": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        "PHONE": r'(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',
        "SSN_US": r'\d{3}-\d{2}-\d{4}',
    }

    def scrub_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Scans object columns for PII and replaces matches with [REDACTED].
        Returns a new cleaned dataframe.
        """
        df_clean = df.copy()
        
        # Only check object/string columns to save perf
        string_cols = df_clean.select_dtypes(include=['object', 'string']).columns
        
        for col in string_cols:
            for pii_type, pattern in self.PATTERNS.items():
                # Check 1% sample to see if column likely contains this PII type?
                # For safety, we just allow regex replacement.
                # Note: This is an expensive operation for large DFs, but safety first.
                
                # Check if column name itself suggests PII
                if pii_type.lower() in col.lower():
                     df_clean[col] = "[REDACTED_COL]"
                     continue

                # Content scan
                mask = df_clean[col].astype(str).str.contains(pattern,  regex=True, na=False)
                if mask.any():
                    # Replace regex matches
                    df_clean[col] = df_clean[col].astype(str).str.replace(pattern, f"[REDACTED_{pii_type}]", regex=True)
                    
        return df_clean

class LogSanitizer:
    """
    Removes sensitive keys from dictionaries before logging.
    """
    SENSITIVE_KEYS = {"password", "token", "secret", "auth", "api_key", "ssn", "credit_card"}

    @staticmethod
    def sanitize(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively sanitizes a dictionary.
        """
        clean_data = {}
        for k, v in data.items():
            if k.lower() in LogSanitizer.SENSITIVE_KEYS:
                clean_data[k] = "***REDACTED***"
            elif isinstance(v, dict):
                clean_data[k] = LogSanitizer.sanitize(v)
            elif isinstance(v, list):
                 clean_data[k] = [LogSanitizer.sanitize(i) if isinstance(i, dict) else i for i in v]
            else:
                clean_data[k] = v
        return clean_data
