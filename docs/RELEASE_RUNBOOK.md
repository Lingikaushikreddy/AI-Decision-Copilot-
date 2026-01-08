# Release Runbook

**Service**: AI Decision Copilot
**Owner**: Platform Engineering Team

## 1. Release Process
### Prerequisite
- Ensure all tests pass: `pytest tests/`
- Ensure security scan passes: `bandit -r backend/`
- Docker build succeeds: `docker build .`

### Deployment (Docker)
1. **Build**: `docker build -t decision-copilot:v1.0.0 .`
2. **Push**: `docker push registry.internal/decision-copilot:v1.0.0`
3. **Deploy**: Update Kubernetes manifest or `docker-compose.yml` with new tag.

### Rollback Strategy
If `error_rate > 1%` or `latency_p99 > 2s`:
1. **Revert**: `kubectl rollout undo deployment/copilot-backend`
2. **Verify**: Check `/health` endpoint.
3. **Debug**: Inspect logs via `docker logs <container_id>`.

## 2. Observability
### Key Metrics (Prometheus)
- `http_requests_total`: Traffic volume.
- `http_request_duration_seconds`: Latency (P50, P90, P99).
- `llm_token_usage_total`: Cost driver (monitor closely).
- `model_inference_errors_total`: Quality signal.

### Alerts
- **High Latency**: P99 > 5s for 5m -> **Page On-Call**
- **High Error Rate**: > 5% errors for 5m -> **Page On-Call**
- **Token Spike**: > 1M tokens/hour -> **Slack Alert #fin-ops**

## 3. Maintenance
- **Log Rotation**: Logs are rotated daily.
- **Database Backup**: Nightly snapshots of `audit_trail` (if moved to DB).
