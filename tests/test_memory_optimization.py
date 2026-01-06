import asyncio
import pytest
from fastapi import UploadFile
from backend.services.ingestion_service import IngestionService
import os

@pytest.mark.asyncio
async def test_large_file_processing():
    service = IngestionService()
    filename = "test_large.csv"
    
    # Ensure file exists (created by previous shell command)
    if not os.path.exists(filename):
        pytest.skip("Large file not found")

    print(f"Testing with file: {filename} ({os.path.getsize(filename) / 1024 / 1024:.2f} MB)")
    
    with open(filename, "rb") as f:
        # Mock UploadFile
        mock_file = UploadFile(filename=filename, file=f)
        
        # This calls the method we optimized
        result = await service.process_file(mock_file)
        
    print(f"Result: {result}")
    assert result["row_count"] >= 1000000
    assert result["health_score"] > 0
