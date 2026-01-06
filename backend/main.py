from fastapi import FastAPI
from backend.routers import ingest, workflow
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("audit_trail")

app = FastAPI(title="AI Decision Copilot API", version="1.0.0")

# Include routers
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "decision-copilot-backend"}

@app.middleware("http")
async def audit_middleware(request, call_next):
    response = await call_next(request)
    logger.info(f"AUDIT: {request.method} {request.url} - Status: {response.status_code}")
    return response
