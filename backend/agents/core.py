from backend.agents.prompts import QUESTIONING_AGENT_PROMPT, SCENARIO_AGENT_PROMPT, MEMO_AGENT_PROMPT
from backend.agents.memory import memory_store
import json

# Mock LLM Call Wrapper
async def mock_llm_call(system_prompt: str, user_context: str):
    # In a real system, this would call OpenAI/Gemini
    # Here we return deterministic mock responses based on the prompt type
    
    if "Must-Ask" in system_prompt:
        return json.dumps([
            {"question": "Is the increase in marketing spend for Q3 confirmed?", "rationale": "High variance detected in Q3 projections.", "impact_score": 9},
            {"question": "Do we have a hiring freeze in place for Engineering?", "rationale": "Staff costs flatline while headcount target increases.", "impact_score": 8}
        ])
    
    if "What-If" in system_prompt:
        return json.dumps({
            "conservative": {"marketing_cut": "10%", "hiring_freeze": True},
            "aggressive": {"marketing_increase": "20%", "hiring_freeze": False},
            "balanced": {"marketing_flat": True, "hiring_slowdown": True}
        })

    if "Decision Memo" in system_prompt:
        return "BLUF: Proceed with the Balanced Plan. \n\nEvidence: Maintains positive cash flow while allowing critical hires."
    
    return "I am unsure."

class QuestioningAgent:
    async def analyze(self, data_profile: dict):
        context = f"Data Profile: {json.dumps(data_profile)}\nMemory: {memory_store.get_context()}"
        response = await mock_llm_call(QUESTIONING_AGENT_PROMPT, context)
        return json.loads(response)

class ScenarioAgent:
    async def suggest_scenarios(self, constraints: list):
        context = f"Constraints: {constraints}\nMemory: {memory_store.get_context()}"
        response = await mock_llm_call(SCENARIO_AGENT_PROMPT, context)
        return json.loads(response)

class MemoAgent:
    async def write_memo(self, simulation_results: dict):
        context = f"Results: {json.dumps(simulation_results)}\nMemory: {memory_store.get_context()}"
        response = await mock_llm_call(MEMO_AGENT_PROMPT, context)
        return response
