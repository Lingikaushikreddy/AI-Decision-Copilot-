# Compliance Checklist

This checklist ensures the AI Decision Copilot meets standard enterprise security and privacy requirements (GDPR, CCPA, SOC2 Type I readiness).

## Data Privacy (GDPR/CCPA)
- [x] **Right to be Forgotten**: Implementation of `DELETE /data/{user_id}` API to remove user artifacts.
- [x] **Data Minimization**: Temporary file handling ensures raw data is not persisted longer than necessary for processing.
- [x] **PII Detection**: Ingestion service proactively scans for Emails, Phones, and SSNs to warn users of sensitive data upload.
- [ ] **Consent Management**: (To be implemented in Frontend) User must agree to Terms before upload.

## Access Control & Authentication
- [x] **Role-Based Access Control (RBAC)**: Structure for Admin vs User endpoints established.
- [ ] **MFA**: (Dependent on Identity Provider integration).
- [x] **Session Management**: APIs are stateless; ready for JWT integration.

## Auditing & Logging
- [x] **Audit Trail**: Centralized `audit_trail.jsonl` records all key business events (Ingest, Simulate, Delete).
- [x] **Log Sanitation**: Sensitive fields (passwords, tokens) are automatically redacted from logs.
- [ ] **Log Retention**: Log rotation policy (currently append-only).

## Data Security
- [x] **Encryption in Transit**: (Assumed TLS termination at Load Balancer/Reverse Proxy).
- [ ] **Encryption at Rest**: (Not applicable for ephemeral storage, but OS-level encryption recommended for deployment).
- [x] **Input Validation**: Strict type checking and PII scanning on file uploads.
- [x] **Availability**: Streaming processing prevents memory-based DoS attacks.

## Software Development Lifecycle (SDLC)
- [x] **Code Review**: All changes go through PR review.
- [x] **Testing**: Automated unit tests for backend logic.
- [x] **Dependency Management**: Standardized `requirements.txt` and environment isolation.
