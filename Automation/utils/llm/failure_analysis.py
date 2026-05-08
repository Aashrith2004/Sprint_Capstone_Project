"""
utils/llm/failure_analysis.py
"""

from utils.logger import get_logger

logger = get_logger(__name__)


def analyze_failure(
    error_message: str
):
    """
    MCP-inspired AI failure analysis.
    """

    logger.info(
        f"Analyzing failure: {error_message}"
    )

    error_message = error_message.lower()

    if "nosuchelementexception" in error_message:

        return (
            "AI Suggestion: "
            "Locator may have changed."
        )

    elif "timeoutexception" in error_message:

        return (
            "AI Suggestion: "
            "Increase explicit wait timeout."
        )

    elif "staleelementreferenceexception" in error_message:

        return (
            "AI Suggestion: "
            "DOM refreshed dynamically."
        )

    elif "elementclickinterceptedexception" in error_message:

        return (
            "AI Suggestion: "
            "Element blocked by overlay."
        )

    return (
        "AI Suggestion: "
        "Unknown automation issue."
    )