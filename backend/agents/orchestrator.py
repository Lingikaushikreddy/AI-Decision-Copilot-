from backend.agents.core import QuestioningAgent, ScenarioAgent, MemoAgent
from backend.agents.memory import memory_store

class AgentOrchestrator:
    def __init__(self):
        self.questioner = QuestioningAgent()
        self.scenarist = ScenarioAgent()
        self.writer = MemoAgent()

    async def run_analysis_workflow(self, data_profile: dict):
        # 1. Check Data Quality & Ask Questions
        questions = await self.questioner.analyze(data_profile)
        
        # 2. (Simulated functionality) Auto-inject constraint if high confidence
        # In real app, user answers would populate memory
        memory_store.add_constraint("Budget Cap: $5M")
        
        return {
            "status": "needs_clarification" if questions else "ready",
            "questions": questions,
            "context_used": memory_store.get_context()
        }

    async def run_decision_workflow(self, simulation_results: dict):
        # 1. Generate Memo
        memo = await self.writer.write_memo(simulation_results)
        return {"memo": memo}
