# Security Threat Model (STRIDE)

**System**: AI Decision Copilot
**Date**: 2026-01-08

## 1. System Overview
The AI Decision Copilot ingests simplified financial data (CSVs), runs simulations, and uses an LLM to generate executive decision memos. It is designed for internal enterprise use.

## 2. STRIDE Analysis

| Category | Threat | Mitigation | Status |
| :--- | :--- | :--- | :--- |
| **S**poofing | User impersonating an Admin to delete data. | No Authentication in MVP (Risk Accepted). Internal network only. | ⚠️ Low |
| **T**ampering | User modifying the "Audit Trail" file on disk. | File system permissions + Append-only log logic (Soft control). | ⚠️ Medium |
| **R**epudiation | User claiming "I didn't run that risky simulation". | **AuditLogger** tracks every `sim_run` with timestamp and params. | ✅ Mitigated |
| **I**nformation Disclosure | **PII Leakage**: Uploading a CSV with "Employee Names" or "SSNs" to the LLM. | **PIIScrubber** (Regex-based) runs at ingestion. Redacts emails/phones. | 🔄 In Progress |
| **I**nformation Disclosure | **Log Leakage**: Sensitive data (e.g. API keys, salaries) printed in server logs. | **LogSanitizer** filters sensitive keys before writing to disk. | 🔄 In Progress |
| **D**enial of Service | **CSV Bomb**: Uploading a 10GB file to crash memory. | **Stream Processing** (already implemented) + File Size Limits (100MB). | ✅ Mitigated |
| **E**levation of Privilege | Standard user deleting other users' datasets. | Data is session-based / ephemeral in MVP currently. | ℹ️ N/A |

## 3. Compliance & Privacy (GDPR/CCPA)
- **Right to be Forgotten**: We must support deleting all artifacts related to a specific `user_id`.
- **Data Minimization**: Only ingest columns necessary for simulation.

## 4. Action Items
1. [ ] Implement `PIIScrubber` to scan uploaded DataFrames.
2. [ ] Implement `LogSanitizer` for Audit Middleware.
3. [ ] Build `DELETE /api/admin/data` endpoint.
