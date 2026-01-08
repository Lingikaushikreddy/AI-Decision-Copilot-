from fastapi import FastAPI
from backend.routers import ingest, workflow, admin
from backend.services.audit_service import audit_logger
from backend.services.security import LogSanitizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Decision Copilot API", version="1.0.0")

# Include routers
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin/Compliance"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Middleware for Audit Logging
@app.middleware("http")
async def audit_middleware(request, call_next):
    response = await call_next(request)
    
    # Sanitize details before logging
    raw_details = {
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "headers": dict(request.headers) # Headers often contain auth tokens
    }
    safe_details = LogSanitizer.sanitize(raw_details)

    # Log to audit file using the service
    audit_logger.log_event(
        user_id="system", # placeholder
        action="HTTP_REQUEST",
        details=safe_details
    )
    return response
