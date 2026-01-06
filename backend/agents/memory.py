import json
import logging
from typing import Dict, Any

logger = logging.getLogger("agent_memory")

class AssumptionMemory:
    def __init__(self):
        self._store: Dict[str, Any] = {
            "global_constraints": [],
            "definitions": {},
            "user_preferences": {}
        }

    def add_constraint(self, rule: str):
        if rule not in self._store["global_constraints"]:
            self._store["global_constraints"].append(rule)
            logger.info(f"Memory Updated: Added constraint '{rule}'")

    def define_term(self, term: str, definition: str):
        self._store["definitions"][term] = definition
        logger.info(f"Memory Updated: Defined '{term}'")

    def get_context(self) -> str:
        return json.dumps(self._store, indent=2)

    def clear(self):
        self._store = {
            "global_constraints": [],
            "definitions": {},
            "user_preferences": {}
        }

# Singleton
memory_store = AssumptionMemory()
