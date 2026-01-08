# AI Decision Copilot - Threat Model

## 1. System Overview
The AI Decision Copilot is a web-based analytics tool that ingests business data (CSV/Excel), processes it using Python/Pandas, and provides AI-driven insights. It is designed for enterprise users who may upload sensitive financial or operational data.

## 2. Trust Boundaries
*   **External User Browser**: Untrusted input source.
*   **API Gateway (FastAPI)**: Boundary between public internet and internal logic.
*   **File System**: Ephemeral storage for processing.
*   **LLM Service**: External dependency (assumed secure channel).

## 3. Identified Threats & Mitigations (STRIDE)

### Spoofing
*   **Threat**: Attacker impersonates a legitimate user to access data.
*   **Mitigation**: (Future) Enforce robust Authentication (OAuth2/SSO) and verify JWTs on every request. Currently reliant on deployment environment security.

### Tampering
*   **Threat**: Malicious CSV upload containing script injection (CSV Injection) or excessive size (DoS).
*   **Mitigation**:
    *   **Input Validation**: `IngestionService` validates file extension and structure.
    *   **Streaming Processing**: Process CSVs in chunks to prevent memory exhaustion (DoS).
    *   **Sanitization**: All inputs to LLM prompts are treated as untrusted.

### Repudiation
*   **Threat**: Admin deletes data or User performs sensitive action, then denies it.
*   **Mitigation**:
    *   **Audit Logging**: `AuditLogger` records all critical actions (Upload, Delete, Simulation) with timestamps and user IDs.
    *   **Secure Logs**: Sensitive data (passwords/tokens) is redacted from logs to prevent secondary leakage.

### Information Disclosure
*   **Threat**: PII (Email, SSN) in uploaded datasets is leaked to the LLM or displayed in the UI.
*   **Mitigation**:
    *   **PII Detection**: `IngestionService` scans uploads for PII patterns (Email, Phone, SSN) and flags them as anomalies.
    *   **Data Minimization**: Only aggregate data or relevant snippets are sent to the LLM, not raw PII-laden rows.
    *   **Error Handling**: Generic error messages to users; detailed stack traces only in secure server logs.

### Denial of Service
*   **Threat**: Uploading a "zip bomb" or massive CSV to crash the server.
*   **Mitigation**:
    *   **Streaming**: Chunk-based processing.
    *   **Timeouts**: API timeouts.
    *   **File cleanup**: Temp files are deleted immediately after processing (`finally` block in `IngestionService`).

### Elevation of Privilege
*   **Threat**: User accesses Admin API (e.g., `DELETE /data/{id}`).
*   **Mitigation**:
    *   **RBAC Stub**: Admin endpoints check for admin privileges (to be fully enforced with Auth integration).
    *   **Path Traversal Check**: `delete_user_data` validates `user_id` to prevent deleting system files.

## 4. Compliance Controls (GDPR/CCPA)
*   **Right to be Forgotten**: `DELETE /data/{user_id}` endpoint implemented.
*   **Data Minimization**: Retention policy focuses on ephemeral processing; no long-term storage of raw user uploads without consent.
*   **Auditability**: All processing events are logged.
