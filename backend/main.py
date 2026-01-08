from fastapi import FastAPI
from backend.routers import ingest, workflow, admin
from backend.services.audit_service import audit_logger
from backend.services.security import LogSanitizer
from backend.services.monitoring import router as metrics_router, monitor
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(title="AI Decision Copilot API", version="1.0.0")

# Include routers
app.include_router(ingest.router, prefix="/api/ingest", tags=["Ingestion"])
app.include_router(workflow.router, prefix="/api/workflow", tags=["Workflow"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin/Compliance"])
app.include_router(metrics_router, tags=["Observability"])

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Middleware for Audit Logging & Monitoring
@app.middleware("http")
async def app_middleware(request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # 1. Monitoring (Metrics)
    # Avoid high-cardinality for endpoints with IDs, simple heuristic for now
    endpoint = request.url.path
    monitor.track_request(request.method, endpoint, response.status_code)
    monitor.track_latency(request.method, endpoint, process_time)
    
    # 2. Audit Logging (Security)
    # Sanitize details before logging
    raw_details = {
        "method": request.method,
        "url": str(request.url),
        "status_code": response.status_code,
        "duration_ms": round(process_time * 1000, 2)
    }
    safe_details = LogSanitizer.sanitize(raw_details)

    audit_logger.log_event(
        user_id="system", 
        action="HTTP_REQUEST",
        details=safe_details
    )
    
    return response
