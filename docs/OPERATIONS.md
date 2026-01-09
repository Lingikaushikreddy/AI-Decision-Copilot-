# Operational Runbook

This document outlines the procedures for deploying, monitoring, and maintaining the AI Decision Copilot platform.

## Deployment

The platform is containerized using Docker.

### Prerequisites

- Docker
- Docker Compose

### Building and Running

To start the full stack (Backend + Frontend + Prometheus):

```bash
docker-compose up --build
```

The services will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:5173
- Prometheus: http://localhost:9090

### Production Deployment

For production, the `Dockerfile` is optimized for the backend service. The frontend should be built separately (using `npm run build`) and served via a static file host (e.g., Nginx, Vercel, S3+CloudFront).

## Monitoring

We use **Prometheus** for metrics collection.

### Key Metrics

- `http_requests_total`: Total request count by method, endpoint, and status.
- `http_request_duration_seconds`: Latency distribution.
- `llm_token_usage_total`: Token consumption for cost tracking.
- `model_inference_errors_total`: Failure rates for AI models.

### Accessing Metrics

- Raw metrics: http://localhost:8000/metrics
- Prometheus UI: http://localhost:9090

## Rollback Strategy

In case of a deployment failure or critical bug, follow this rollback procedure:

1.  **Identify the Last Known Good Version**:
    - Check the GitHub Actions run history to find the Commit SHA of the last successful build.
    - Docker images are tagged with `sha-<COMMIT_SHA>`.

2.  **Revert Deployment**:
    - **If using Kubernetes/Helm**: Update the deployment manifest to point to the previous image tag.
      ```bash
      kubectl set image deployment/decision-copilot-api api=registry.example.com/decision-copilot:sha-OLD_SHA
      ```
    - **If using Docker Compose**: Update `.env` or `docker-compose.yml` to use the specific tag and restart.
      ```bash
      IMAGE_TAG=sha-OLD_SHA docker-compose up -d
      ```

3.  **Verify Rollback**:
    - Check `/health` endpoint.
    - Monitor error rates in Prometheus to ensure stability.

## Model & Prompt Management

Prompts are managed via configuration files to allow updates without full code redeployment (if mounted as config maps).

- **Location**: `backend/config/prompts.yaml`
- **Versioning**: Each prompt entry can have a version field. To roll back a prompt, revert the change in the YAML file.
