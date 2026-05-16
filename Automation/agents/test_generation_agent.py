"""
Agent: TestGenerationAgent
Generates pytest + Selenium test scripts from plain-English requirements.
Integrates with your existing pages/, fixtures/, and utils/ structure.
"""

from utils.llm.llm_helper import call_llm
from utils.llm.prompt_builder import build_test_generation_prompt
from utils.logger import get_logger

logger = get_logger(__name__)


class TestGenerationAgent:
    """
    AI agent that converts a plain-English testing requirement into a
    fully runnable pytest + Selenium script, pre-wired to your project's
    page objects and fixtures.
    """

    def generate_test(self, requirement: str) -> str:
        logger.info("TestGenerationAgent: generating test for requirement")
        prompt = build_test_generation_prompt(requirement)
        result = call_llm(prompt)
        logger.info("TestGenerationAgent: generation complete")
        return result