from fastapi import FastAPI
from backend.routers import ingest, workflow
from backend.services.audit_service import audit_logger
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Decision Copilot API", version="1.0.0")

# Include routers
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Middleware for Audit Logging
@app.middleware("http")
async def audit_middleware(request, call_next):
    response = await call_next(request)
    # Log to audit file using the service
    audit_logger.log_event(
        user_id="system", # placeholder
        action="HTTP_REQUEST",
        details={
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code
        }
    )
    return response
