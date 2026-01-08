
- **Workflow**: End-to-end integration tests mocking the database and agent responses.

### Security Engineering (Enterprise Readiness)
#### [NEW] `backend/services/security.py`
- **PIIScrubber**: Regex-based detection for emails, phones, SSNs in uploaded data.
- **LogSanitizer**: Filters sensitive keys (`password`, `token`, `pii_field`) from Audit Logs.

#### [NEW] `backend/routers/admin.py`
- **Data Deletion**: Compliance endpoint (`DELETE /api/admin/data/{user_id}`) for GDPR/CCPA "Right to be Forgotten".

#### [NEW] `docs/ThreatModel.md`
- STRIDE analysis of the system (Spoofing, Tampering, Repudiation, etc.).

## Verification Plan
### Automated Tests
- `pytest` for API endpoint validation (ingest, scenario calculation).
- `tests/test_simulation.py`: Verify statistical correctness (e.g., Mean of Monte Carlo ~ Deterministic Mean).
- `tests/test_explainability.py`: Verify that drivers are correctly ranked and evidence links are generated.
- `tests/test_agents.py`: Mock LLM responses to verify orchestration logic (e.g., ensure QuestioningAgent is triggered when Data Health < 80).
- `tests/test_security.py`: Verify PII masking and Admin endpoint.
- Run `npm run build` to verify clean frontend build.

### Manual Verification
- Review against "Real-world constraints" requirement.
- Ensure "dumb" questions are avoided and "must-ask" questions are included.
- Verify UI designs include requested "Trust Cues" (confidence scores, citations).
