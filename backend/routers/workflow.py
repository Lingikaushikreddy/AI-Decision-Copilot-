from fastapi import APIRouter, HTTPException
from backend.services.workflow_service import WorkflowService
from pydantic import BaseModel

router = APIRouter()
service = WorkflowService()

class ScenarioParams(BaseModel):
    marketing_spend_delta: float
    hiring_freeze: bool

class SimulationResult(BaseModel):
    baseline_cash: list[float]
    scenario_cash: list[float]
    savings_impact: float

class MemoRequest(BaseModel):
    scenario_id: str
    decision_type: str

@router.post("/simulate", response_model=SimulationResult)
async def run_simulation(params: ScenarioParams):
    try:
        return service.run_simulation(params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/memo")
async def generate_memo(request: MemoRequest):
    return service.generate_memo(request.scenario_id, request.decision_type)
