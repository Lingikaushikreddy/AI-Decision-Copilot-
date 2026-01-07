import pandas as pd
from fastapi import UploadFile
import shutil
import tempfile
import os
import logging

logger = logging.getLogger("ingest_service")

class IngestionService:
    async def process_file(self, file: UploadFile):
        # 1. Spool to temp file to avoid RAM spike (Fix for 54GB memory issue)
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        try:
            logger.info(f"Processing file streamed to disk: {tmp_path}")
            if suffix.lower() == '.csv':
                return self._profile_csv_stream(tmp_path, file.filename)
            else:
                # Excel is harder to stream, fallback to load (usually smaller than CSVs)
                df = pd.read_excel(tmp_path)
                return self._profile_dataframe(df, file.filename)
        except pd.errors.EmptyDataError:
             return {"filename": file.filename, "row_count": 0, "health_score": 0, "anomalies": ["Empty File"], "schema": {}}
        except Exception as e:
            logger.error(f"Error processing file: {str(e)}")
            # If it's a parsing error that we can catch (like UnicodeDecodeError or ParserError),
            # we might want to return a specific profile indicating failure, or re-raise.
            # But the requirement is "Doesn't break".
            if isinstance(e, (UnicodeDecodeError, pd.errors.ParserError)):
                 # Return a "Broken File" profile
                 return {
                     "filename": file.filename,
                     "row_count": 0,
                     "health_score": 0,
                     "anomalies": ["Unreadable file format or corrupted content"],
                     "schema": {}
                 }
            raise e
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
                logger.info("Cleaned up temp file")

    def _profile_csv_stream(self, filepath: str, filename: str):
        """
        Profiles CSV in chunks to keep memory usage low (< 100MB).
        """
        chunk_size = 5000
        total_rows = 0
        missing_counts = {}
        anomalies = []
        schema = {}
        
        first_chunk = True
        
        # Stream through the file
        with pd.read_csv(filepath, chunksize=chunk_size) as reader:
            for chunk in reader:
                # 1. Schema Inference (from first chunk)
                if first_chunk:
                    chunk = chunk.convert_dtypes()
                    for col in chunk.columns:
                        schema[col] = str(chunk[col].dtype)
                        missing_counts[col] = 0
                    first_chunk = False
                
                # 2. Update Aggregates
                total_rows += len(chunk)
                
                # Count missing per column
                chunk_missing = chunk.isnull().sum()
                for col, count in chunk_missing.items():
                    if col in missing_counts:
                        missing_counts[col] += count
                
                # Sample anomalies (limit to first 10 occurrences found)
                if len(anomalies) < 10:
                    numeric_cols = chunk.select_dtypes(include=['number']).columns
                    for col in numeric_cols:
                        if (chunk[col] < 0).any():
                            anomalies.append(f"Negative values detected in column '{col}'")
                            if len(anomalies) >= 10: break

        # 3. Calculate Final Health Score
        total_cells = total_rows * len(schema)
        if total_cells == 0:
            return {"filename": filename, "row_count": 0, "health_score": 0, "anomalies": ["Empty File"], "schema": {}}

        total_missing = sum(missing_counts.values())
        health_score = max(0, int(100 - ((total_missing + len(anomalies) * 100) / total_cells * 1000))) 
        # Heuristic: Penalize missing data (weighted)

        return {
            "filename": filename,
            "row_count": total_rows,
            "health_score": health_score,
            "anomalies": list(set(anomalies))[:10],
            "schema": schema
        }

    def _profile_dataframe(self, df: pd.DataFrame, filename: str):
        # Fallback for Excel
        row_count = len(df)
        if row_count == 0:
             return {"filename": filename, "row_count": 0, "health_score": 0, "anomalies": ["Empty File"], "schema": {}}
        
        anomalies = []
        schema = {col: str(df[col].dtype) for col in df.columns}
        missing = df.isnull().sum().sum()
        
        # Simple negative check
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            if (df[col] < 0).any():
                anomalies.append(f"Negative values detected in column '{col}'")

        total_cells = row_count * len(df.columns)
        health_score = max(0, int(100 - (missing / total_cells * 500)))

        return {
            "filename": filename,
            "row_count": row_count,
            "health_score": health_score,
            "anomalies": anomalies[:10],
            "schema": schema
        }
