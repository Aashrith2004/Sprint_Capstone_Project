"""
tools/file_writer.py
Saves AI-generated test scripts to the generated_tests/ folder.
"""

import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

GENERATED_TESTS_DIR = os.path.join(os.path.dirname(__file__), "..", "generated_tests")


def save_test_file(content: str, prefix: str = "test_ai_") -> str:
    """
    Save generated test content to generated_tests/ with a timestamped filename.
    Returns the full path of the saved file.
    """
    os.makedirs(GENERATED_TESTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{prefix}{timestamp}.py"
    filepath = os.path.join(GENERATED_TESTS_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Generated test saved: %s", filepath)
    return filepath