from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
from fastapi import APIRouter, Response

# --- Metrics Definitions ---
REQUEST_COUNT = Counter(
    'http_requests_total', 
    'Total HTTP requests', 
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency in seconds',
    ['method', 'endpoint']
)

TOKEN_USAGE = Counter(
    'llm_token_usage_total',
    'Total LLM tokens consumed',
    ['model', 'type'] # type=prompt|completion
)

MODEL_ERRORS = Counter(
    'model_inference_errors_total',
    'Total AI Model failures'
)

# --- Service Class ---
class MonitoringService:
    def track_request(self, method: str, endpoint: str, status: int):
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()

    def track_latency(self, method: str, endpoint: str, duration: float):
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    def track_tokens(self, usage: int, model: str = "gpt-4"):
        # Simplified tracking
        TOKEN_USAGE.labels(model=model, type="total").inc(usage)

monitor = MonitoringService()

# --- Router for scraping ---
router = APIRouter()

@router.get("/metrics")
async def metrics():
    """
    Exposes Prometheus metrics for scraping.
    """
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
