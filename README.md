# AI Decision Copilot 🧠

> **The OS for Strategic Decision Making.**
> Turn messy data into "Executive-Ready" memos with probabilistic modeling and agentic reasoning.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/frontend-React_18-61DAFB.svg)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688.svg)
![Python](https://img.shields.io/badge/python-3.10+-3776AB.svg)
![Coverage](https://img.shields.io/badge/tests-passing-brightgreen.svg)

## 🚀 Overview
**AI Decision Copilot** transforms the traditional FP&A workflow. Instead of static spreadsheets, it provides a dynamic, agent-driven interface to:
1.  **Ingest & Profile**: Instantly detect anomalies in financial datasets (Revenue, Costs, Headcount).
2.  **Model Uncertainty**: Run 1000+ Monte Carlo simulations to find P10/P90 confidence intervals.
3.  **Stress Test**: Automatically check business health against "Recession" or "Inflation" scenarios.
4.  **Synthesize**: Generate succinct, evidence-based Decision Memos using a multi-agent LLM system.

---

## ✨ Key Features

### 1. 📊 Intelligent Ingestion
- **Stream Processing**: Handles large datasets (1M+ rows) with <100MB RAM footprint.
- **Auto-Health Check**: Scores data quality (0-100) based on missingness, outliers, and type consistency.

### 2. 🧪 Science-Backed Simulation Engine
- **Monte Carlo**: Simulates probabilistic outcomes (e.g., Revenue +/- 10%) to quantify risk.
- **Break-even Analysis**: Calculates exact "failure points" (e.g., "Cash flow turns negative if Revenue drops < $30k").
- **Constraint Enforcement**: Respects hard business rules (e.g., "Marketing Spend cannot exceed $50k").

### 3. 🤖 Agentic Reasoning Layer
- **Questioning Agent**: Detects ambiguity and asks "Must-Ask" clarifying questions.
- **Scenario Agent**: Suggests "Conservative" vs "Aggressive" plans based on constraints.
- **Memo Agent**: Drafts BLUF (Bottom Line Up Front) memos suitable for C-level review.

---

## 🛠️ Architecture

```mermaid
graph TD
    User[User Upload] --> Ingest[Ingestion Service (Stream)]
    Ingest --> Profile[Data Profiling & Health Score]
    Profile --> QA[Questioning Agent]
    QA --> Context[Assumption Memory]
    Context --> Sim[Simulation Engine (Monte Carlo)]
    Sim --> Risk[Risk Analyzer (Breakpoints)]
    Risk --> Memo[Memo Agent]
    Memo --> UI[Decision Memo UI]
```

## ⚡ Quick Start

### Backend (Python/FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```
*Runs on http://localhost:8000*

### Frontend (React/Vite)
```bash
npm install
npm run dev
```
*Runs on http://localhost:5173*

## 🧪 Running Tests
We maintain high test coverage for the Science and Agent layers.

```bash
# Run Simulation & Risk Engine tests
python3 -m pytest tests/test_simulation.py tests/test_risk_extended.py

# Run Agent Logic tests
python3 -m pytest tests/test_agents.py
```

## 📂 Project Structure
```text
├── backend/
│   ├── agents/         # AI Logic (Prompts, Orchestrator, Memory)
│   ├── engine/         # Physics of Decision (Simulation, Risk, Math)
│   ├── routers/        # API Endpoints
│   └── services/       # Core Business Logic (ETL, Audit)
├── src/                # React Frontend
│   ├── components/     # UI Components (Scenario Builder, Smart Questions)
│   └── ...
└── docs/               # Detailed Product & Technical Documentation
```

## 📄 License
MIT License. Built with ❤️ for Decision Makers.
