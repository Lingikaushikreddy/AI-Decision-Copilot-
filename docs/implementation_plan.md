# Product Documentation Implementation Plan

## Goal Description
Create a comprehensive set of product documents for the "AI Decision Copilot" focusing on Finance, Ops, and Growth managers. This includes a PRD, Roadmap, User Stories, and Success Metrics Dashboard.

## Proposed Changes
### Domain Logic
#### [NEW] [DecisionPlaybook.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/DecisionPlaybook.md)
- "Exec-ready" decision logic for Finance, Ops, and Growth.
- Defines "Good Decision" criteria and trade-offs.
- Validates scenario levers and questions.

#### [NEW] [ConstraintLibrary.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/ConstraintLibrary.md)
- Hard and soft constraints (Budget caps, Compliance, Capacity).

#### [NEW] [KPIDefinitions.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/KPIDefinitions.md)
- Strict business definitions for metrics to ensure data integrity.

### UX/UI Design
#### [NEW] [UserJourneyMap.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/UserJourneyMap.md)
- End-to-end flow: Upload -> Analysis -> Decision.

#### [NEW] [UISpecs.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/UISpecs.md)
- Detailed screen layouts, component states, and trust cues.

#### [NEW] [UsabilityFindings.md](file:///Users/kaushikreddy/.gemini/antigravity/brain/25af075f-8b0e-4991-8334-2a373758b598/UsabilityFindings.md)
- Mock research results from 5 user sessions.

#### [IMAGE] UI Mockups
- Will generate visualizations for "Scenario Builder" and "Decision Memo" screens using `generate_image`.

### Frontend Engineering (React)
#### [NEW] [ai-decision-copilot-ui] (Directory)
- Initialize new Vite + React + TypeScript project in `/Users/kaushikreddy/Desktop/AI Decision Copilot`.
- Stack: React, Tailwind CSS, Recharts (for analytics), Lucide React (icons).

#### [NEW] Component Architecture
- `components/ingest/`: `FileUploader.tsx`, `DataHealthSummary.tsx`
- `components/analysis/`: `SmartQuestions.tsx`, `RankingPanel.tsx`
- `components/scenarios/`: `ScenarioBuilder.tsx` (Sliders), `ComparisonChart.tsx`
- `components/output/`: `DecisionMemo.tsx`, `RiskGauge.tsx`

### Backend Engineering (Python/FastAPI)
#### [NEW] [backend] (Directory)
- **Stack**: Python 3.10+, FastAPI, Pandas (profiling), Pydantic (validation).
- **Structure**:
    - `main.py`: App entry point.
    - `routers/`: `ingest.py` (upload), `workflow.py` (simulations).
    - `services/`: 
        - `IngestionService`: CSV parsing, outlier detection.
        - `Orchestrator`: Manages state between analysis -> decision.
        - `AuditLogger`: JSON-based audit trail for compliance.

### Data Engineering (ETL)
#### [MODIFY] `backend/services/ingestion_service.py`
- Enhance `IngestionService` to support:
    - **Type Inference**: Detect numeric vs categorical columns automatically.
    - **Advanced Profiling**: Skewness, outliers (IQR method), duplicate detection.
    - **Normalization**: Date standardization (ISO8601), Currency sanitization.

#### [NEW] `backend/services/etl_pipeline.py`
- **Output**: Transforms raw DF into "Standard Decision Table" (long format).
- **Structure**: `[entity_id, time, metric_value, metric_name, dimensions]`.
- **Quality Score**: Generates field-level confidence flags.

### AI/ML Agents (LLM Layer)
#### [NEW] `backend/agents/`
- **Architecture**: Multi-agent system (conceptual LangGraph).
- **Core Agents**:
    - `DataQualityAgent`: Reviews ETL output for gaps.
    - `QuestioningAgent`: Uses context to generate ranked clarifying questions.
    - `ScenarioAgent`: Suggests "safe" vs "aggressive" simulation parameters.
    - `MemoAgent`: Synthesizes results into BLUF format.
- **Memory**: `AssumptionStore` (JSON) to track user constraints across sessions.
- **Guardrails**: System prompts enforcing "No hallucination" and "Cite Evidence".

### Decision Modeling & Simulation (Science Layer)
#### [NEW] `backend/engine/`
- **`simulation.py`**:
    - **Base Model**: Deterministic financial calculation (Cash Flow = Revenue - (Fixed + Var Costs)).
    - **Monte Carlo**: Run 1000 iter, perturbing inputs (Revenue +/- 10%, Costs +/- 5%) to generate confidence intervals (P10, P50, P90).
- **`risk.py`**:
    - **Sensitivity**: One-at-a-time analysis (OAT) to find top drivers of variance.
    - **KPI Probability**: Calculate % chance of missing target (e.g., Cash < 0).

#### [MODIFY] `backend/services/workflow_service.py`
- Replace mock logic with:
    ```python
    engine = SimulationEngine(baseline_data)
    results = engine.run_monte_carlo(params, iterations=1000)
    return results.to_dict()
    ```

### Explainability & Analytics (Defendability Layer)
#### [NEW] `backend/engine/explainability.py`
- **`DriverAnalyzer`**:
    - **Top Contributors**: Rank inputs by their impact on variance (using `RiskAnalyzer` sensitivity).
    - **Bridge Chart Logic**: Generate data for a "waterfall" explanation (Baseline -> Volume Effect -> Price Effect -> Result).
- **`EvidenceTracer`**:
    - A lightweight utility to format "Citation" objects linking back to specific input fields or constraints (e.g., "Source: Constraint #3 (Budget Cap)").

#### [MODIFY] `backend/agents/prompts.py`
- Update `MEMO_AGENT_PROMPT` to explicitly request specific sections: "Trade-offs", "Key Risks", "Mitigations".
- Feed `DriverAnalyzer` outputs into the prompt context so the LLM can write: "The main driver of risk is *Marketing Spend*..."

## Verification Plan
### Automated Tests
- `pytest` for API endpoint validation (ingest, scenario calculation).
- `tests/test_simulation.py`: Verify statistical correctness (e.g., Mean of Monte Carlo ~ Deterministic Mean).
- `tests/test_explainability.py`: Verify that drivers are correctly ranked and evidence links are generated.


- `tests/test_agents.py`: Mock LLM responses to verify orchestration logic (e.g., ensure QuestioningAgent is triggered when Data Health < 80).
- Run `npm run build` to verify clean frontend build.

### Manual Verification
- Review against "Real-world constraints" requirement.


- Ensure "dumb" questions are avoided and "must-ask" questions are included.
- Verify UI designs include requested "Trust Cues" (confidence scores, citations).



