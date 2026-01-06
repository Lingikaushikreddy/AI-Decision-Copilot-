# Test Plan: AI Decision Copilot Quality Assurance

## 1. Overview
This document outlines the test strategy for the AI Decision Copilot, focusing on robustness, edge cases, and regression testing. The goal is to ensure the system handles "messy reality" (weird files, broken data, user errors) gracefully.

## 2. Scope
*   **File Ingestion**: Upload validation, parsing resilience, and data profiling.
*   **Workflow Engine**: Simulation calculations and Q&A flow consistency.
*   **Audit & Security**: Event logging and export validation.

## 3. Test Strategy
We will employ a mix of integration tests and unit tests using `pytest`.

### 3.1 Tools
*   **Framework**: `pytest`
*   **Libraries**: `pandas`, `numpy`, `fastapi.testclient`
*   **CI/CD**: Tests should run on every commit.

## 4. Test Cases

### 4.1 Ingestion & Profiling (`backend/routers/ingest.py`, `backend/services/ingestion_service.py`)

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|-----------------|
| ING-01 | Invalid Extension | Upload `.txt`, `.exe`, `.pdf` | 400 Bad Request |
| ING-02 | Empty File | Upload 0kb file | 200 OK with `row_count: 0`, Health: 0 |
| ING-03 | Corrupted CSV | Upload file with garbage binary content renamed to `.csv` | 400/500 (handled gracefully) |
| ING-04 | Missing Headers | CSV with data but no header row | Handled or flagged as anomaly |
| ING-05 | Broken Dates | Dates like `2023-02-31` | Parsed safely (as object) |
| ING-06 | Anomalies | Negative values in numeric columns | Flagged in `anomalies` list |
| ING-07 | Excel Support | Upload valid `.xlsx` | Parsed correctly |

### 4.2 Workflow & Simulation (`backend/routers/workflow.py`, `backend/engine/simulation.py`)

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|-----------------|
| SIM-01 | Basic Run | Run simulation with default params | Returns valid JSON, no crash |
| SIM-02 | Hiring Freeze | Set `hiring_freeze=True` | Operational costs decrease |
| SIM-03 | Marketing Spend | Increase marketing spend | Cash flow updates correctly |
| SIM-04 | Audit Log | Run simulation | Entry created in `audit_trail.jsonl` |

### 4.3 Audit (`backend/services/audit_service.py`)

| ID | Test Case | Description | Expected Result |
|----|-----------|-------------|-----------------|
| AUD-01 | Log Format | specific action | JSONL line with timestamp, user_id, action |

## 5. Execution Plan
1.  Create `tests/conftest.py` for shared fixtures.
2.  Implement `tests/test_ingestion_edge_cases.py`.
3.  Implement `tests/test_workflow_integration.py`.
4.  Run tests and fix identified bugs.
