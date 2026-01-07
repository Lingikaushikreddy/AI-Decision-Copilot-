# QA Test Plan: "Messy Reality" Robustness
**Objective**: Ensure the AI Decision Copilot handles imperfect data, mathematical edge cases, and unexpected inputs gracefully without crashing.

## 1. Data Ingestion (The Front Door)
**Risk**: Users upload weird Excel files, renamed CSVs, or unstructured dumps.
**Tests**:
- [ ] **Empty Files**: 0KB uploads should return specific 400 Error.
- [ ] **Missing Columns**: If 'Revenue' column is missing, soft-fail with "Missing required column" instead of 500 Key Error.
- [ ] **Dirty Types**: "1,000" (string) instead of 1000 (int). "N/A" or "null" in numeric fields.
- [ ] **Binary Garbage**: Uploading a PDF renamed as .csv.

## 2. Simulation & Math Engine (The Core)
**Risk**: Scenarios that break mathematical axioms.
**Tests**:
- [ ] **Divide by Zero**: Profit Margin calculation where Revenue = 0.
- [ ] **Negative Inputs**: Negative "Fixed Costs" (unless explicit refund).
- [ ] **Infinite Scale**: Inputs > 1 Trillion causing float overflow/precision issues.

## 3. Agent Orchesration (The Brain)
**Risk**: LLM context window overflow or empty context.
**Tests**:
- [ ] **Empty Data**: Agents triggered with no analysis context.
- [ ] **Hallucination Triggers**: Scenarios where constraints contradict inputs (e.g. Budget > Revenue).

## 4. Workflows (Integration)
- [ ] **End-to-End**: Ingest Dirty Data -> Clean -> Simulate -> Generate Memo (Should allow flow or error gracefully at specific step).
