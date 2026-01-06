import pytest
import asyncio
from backend.agents.orchestrator import AgentOrchestrator
from backend.agents.memory import memory_store

@pytest.fixture
def orchestrator():
    memory_store.clear()
    return AgentOrchestrator()

@pytest.mark.asyncio
async def test_questioning_agent_trigger(orchestrator):
    """
    Test that the Questioning Agent correctly identifies ambiguity
    and generates questions.
    """
    # Mock data profile with issues
    data_profile = {
        "health_score": 75,
        "anomalies": ["Missing Q3 Data", "High Variance in Marketing Spend"]
    }
    
    result = await orchestrator.run_analysis_workflow(data_profile)
    
    assert result["status"] == "needs_clarification"
    assert len(result["questions"]) > 0
    assert "Is the increase in marketing spend for Q3 confirmed?" in [q["question"] for q in result["questions"]]

@pytest.mark.asyncio
async def test_decision_workflow_memo_generation(orchestrator):
    """
    Test that the Memo Agent synthesizes results into a specific format.
    """
    simulation_results = {
        "baseline_cash": [1000, 1000],
        "scenario_cash": [1200, 1200]
    }
    
    result = await orchestrator.run_decision_workflow(simulation_results)
    
    assert "memo" in result
    assert "BLUF:" in result["memo"]

@pytest.mark.asyncio
async def test_memory_persistence(orchestrator):
    """
    Test that constraints are stored and retrieved from memory.
    """
    memory_store.add_constraint("Test Constraint")
    context = memory_store.get_context()
    
    assert "Test Constraint" in context
