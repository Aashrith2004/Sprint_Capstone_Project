"""
tests/ai/test_ai_generated_note.py
Demonstrates the AI Test Generation Agent integrated into your test suite.
Run: pytest tests/ai/test_ai_generated_note.py -v
"""

import pytest
from agents.test_generation_agent import TestGenerationAgent
from tools.file_writer import save_test_file
from utils.logger import get_logger

logger = get_logger(__name__)


class TestAIGeneratedNote:
    """
    Uses the TestGenerationAgent to generate a pytest+Selenium script
    for note-creation scenarios, then saves it to generated_tests/.
    This test validates that the agent produces non-empty, valid Python.
    """

    def test_agent_generates_create_note_script(self):
        """AI agent generates a test script for the Create Note flow."""
        requirement = """
        Test the Create Note functionality on the Notes App.

        Test Cases:
        - Valid note creation with title and description
        - Note creation with empty title (should show validation error)
        - Note creation with empty description (should show validation error)
        - Verify newly created note appears in the notes list
        """

        agent = TestGenerationAgent()
        generated = agent.generate_test(requirement)

        logger.info("Generated script length: %d chars", len(generated))
        assert generated, "Agent returned empty output"
        assert "def test_" in generated, "Agent output missing test functions"
        assert "import" in generated, "Agent output missing imports"

        file_path = save_test_file(generated, prefix="test_create_note_ai_")
        logger.info("Saved to: %s", file_path)
        assert file_path.endswith(".py")

    def test_agent_generates_login_script(self):
        """AI agent generates a test script for the Login flow."""
        requirement = """
        Test the Login page of the Notes App.

        Test Cases:
        - Valid login with correct email and password
        - Invalid login with wrong password
        - Login with empty email field
        - Login with empty password field
        - Verify redirect to notes dashboard after successful login
        """

        agent = TestGenerationAgent()
        generated = agent.generate_test(requirement)

        assert generated, "Agent returned empty output"
        assert "def test_" in generated

        file_path = save_test_file(generated, prefix="test_login_ai_")
        logger.info("Login script saved to: %s", file_path)

    def test_agent_generates_delete_note_script(self):
        """AI agent generates a test script for the Delete Note flow."""
        requirement = """
        Test the Delete Note functionality.

        Test Cases:
        - Delete an existing note and verify it is removed from the list
        - Cancel delete and verify note still exists
        - Verify delete via API and confirm UI reflects removal
        """

        agent = TestGenerationAgent()
        generated = agent.generate_test(requirement)

        assert generated
        save_test_file(generated, prefix="test_delete_note_ai_")