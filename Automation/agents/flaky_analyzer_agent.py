"""
Agent: FlakyAnalyzerAgent
Analyzes Selenium test failure error messages and identifies root causes.
"""

from utils.llm.llm_helper import call_llm
from utils.llm.prompt_builder import build_flaky_analysis_prompt
from utils.logger import get_logger

logger = get_logger(__name__)


class FlakyAnalyzerAgent:
    """
    AI agent that takes a raw Selenium exception/traceback and returns
    a structured root-cause analysis with recommended fixes.
    """

    def analyze_failure(self, error_message: str) -> str:
        logger.info("FlakyAnalyzerAgent: analyzing failure")
        prompt = build_flaky_analysis_prompt(error_message)
        result = call_llm(prompt)
        logger.info("FlakyAnalyzerAgent: analysis complete")
        return result