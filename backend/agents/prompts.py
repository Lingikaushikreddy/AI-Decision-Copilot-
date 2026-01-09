import yaml
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DEFAULT_GUARDRAILS = """
1. No Hallucinations.
2. Cite Sources.
"""

class PromptRegistry:
    def __init__(self, config_path="backend/config/prompts.yaml"):
        self.config_path = config_path
        self.prompts = {}
        self.guardrails = DEFAULT_GUARDRAILS
        self.load_prompts()

    def load_prompts(self):
        if not os.path.exists(self.config_path):
            logger.warning(f"Prompt config not found at {self.config_path}. Using defaults/fallbacks.")
            return

        try:
            with open(self.config_path, "r") as f:
                data = yaml.safe_load(f)

            self.guardrails = data.get("common", {}).get("guardrails", DEFAULT_GUARDRAILS)

            for key, value in data.get("prompts", {}).items():
                template = value.get("template", "")
                # Inject guardrails if placeholder exists
                if "{GUARDRAILS}" in template:
                    template = template.format(GUARDRAILS=self.guardrails)
                self.prompts[key] = template

        except Exception as e:
            logger.error(f"Failed to load prompt config: {e}")

    def get(self, key, default=None):
        return self.prompts.get(key, default)

# Singleton instance
registry = PromptRegistry()

# Exposed constants for backward compatibility or direct usage
GUARDRAILS = registry.guardrails
QUESTIONING_AGENT_PROMPT = registry.get("questioning_agent", "Error: Prompt 'questioning_agent' not found.")
SCENARIO_AGENT_PROMPT = registry.get("scenario_agent", "Error: Prompt 'scenario_agent' not found.")
MEMO_AGENT_PROMPT = registry.get("memo_agent", "Error: Prompt 'memo_agent' not found.")
