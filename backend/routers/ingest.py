from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.ingestion_service import IngestionService
from pydantic import BaseModel

router = APIRouter()
service = IngestionService()

class DataProfile(BaseModel):
    filename: string
    row_count: int
    health_score: int
    anomalies: list[str]

@router.post("/upload", response_model=DataProfile)
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format. Only CSV/XLSX allowed.")
    
    try:
        profile = await service.process_file(file)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
