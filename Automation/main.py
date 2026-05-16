"""
main.py  —  CLI entry point for the AI QA Agent
Run: python main.py
"""

from agents.test_generation_agent import TestGenerationAgent
from agents.flaky_analyzer_agent import FlakyAnalyzerAgent
from agents.self_healing_agent import SelfHealingAgent
from tools.file_writer import save_test_file


def main():
    # ── 1. Test Generation ──────────────────────────────────────────────────
    requirement = """
    Test the Login page of the Notes App (https://practice.expandtesting.com/notes/app).

    Test Cases:
    - Valid login with correct email and password
    - Invalid login with wrong password
    - Empty email field validation
    - Empty password field validation
    - Verify redirect to /notes after successful login
    """

    print("\n========== STEP 1: TEST GENERATION ==========")
    agent = TestGenerationAgent()
    generated_test = agent.generate_test(requirement)
    print(generated_test)

    file_path = save_test_file(generated_test, prefix="test_login_ai_")
    print(f"\n[INFO] Test saved at: {file_path}")

    # ── 2. Flaky Analysis + Self-Healing ────────────────────────────────────
    error_message = (
        "selenium.common.exceptions.NoSuchElementException: "
        'Unable to locate element: {"method":"css selector","selector":"#login-btn"}\n'
        "  at tests/ui/test_valid_login.py:34"
    )
    failed_locator = 'By.ID, "login-btn"'
    available_dom = (
        '<button id="btn-login" class="login-button" data-testid="login-submit">Login</button>\n'
        '<input id="email-field" name="email" type="email" />\n'
        '<input id="password-field" name="password" type="password" />'
    )

    print("\n========== STEP 2: FLAKY TEST ANALYSIS ==========")
    flaky_agent = FlakyAnalyzerAgent()
    analysis = flaky_agent.analyze_failure(error_message)
    print(analysis)

    print("\n========== STEP 3: SELF-HEALING LOCATOR ==========")
    healing_agent = SelfHealingAgent()
    healing = healing_agent.heal_locator(failed_locator, available_dom)
    print(healing)


if __name__ == "__main__":
    main()