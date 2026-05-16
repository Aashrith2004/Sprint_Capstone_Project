"""
Agent: SelfHealingAgent
Suggests a healed locator when a Selenium element lookup fails.
Works alongside your existing utils/self_healing_locator.py.
"""

from utils.llm.llm_helper import call_llm
from utils.llm.prompt_builder import build_self_healing_prompt
from utils.logger import get_logger

logger = get_logger(__name__)


class SelfHealingAgent:
    """
    AI agent that receives a failed locator + current DOM snapshot and
    recommends the best alternative locator to keep tests green.
    """

    def heal_locator(self, failed_locator: str, available_elements: str) -> str:
        logger.info("SelfHealingAgent: attempting to heal locator: %s", failed_locator)
        prompt = build_self_healing_prompt(failed_locator, available_elements)
        result = call_llm(prompt)
        logger.info("SelfHealingAgent: healing recommendation ready")
        return result