"""
utils/ai/prompt_builder.py
Builds LLM prompts for each agent.
Tailored to your project: pages/login_page.py, pages/notes_page.py,
fixtures/browser_fixture.py, api/auth_api.py, api/notes_api.py.
"""


def build_test_generation_prompt(requirement: str) -> str:
    return f"""You are an expert QA Automation Engineer working on a Python project that uses:
- pytest + Selenium for UI tests
- requests for API tests
- Page Object Model with these existing pages:
    * pages/login_page.py  (LoginPage)
    * pages/notes_page.py  (NotesPage)
    * pages/base_page.py   (BasePage - parent)
- Fixtures in fixtures/browser_fixture.py (fixture name: "driver")
- API clients in api/auth_api.py (AuthAPI) and api/notes_api.py (NotesAPI)
- Config in config/environment.py (BASE_URL, API_URL, credentials)
- Utils: utils/wait_utils.py, utils/logger.py, utils/screenshot.py

Generate a complete, runnable pytest test file based on this requirement:

{requirement}

Rules:
- Import from the correct project modules shown above
- Use the "driver" fixture for UI tests
- Use WebDriverWait for all waits (no time.sleep)
- Add a docstring to each test function
- Return ONLY Python code. No markdown, no explanation.
"""


def build_flaky_analysis_prompt(error_message: str) -> str:
    return f"""You are an expert Selenium test reliability engineer.

Analyze this Selenium test failure from a pytest run and provide a structured response:

ERROR:
{error_message}

Respond with exactly these sections:
1. ROOT CAUSE: (one sentence)
2. CONTRIBUTING FACTORS: (bullet list)
3. RECOMMENDED FIX: (concrete code or config change)
4. PREVENTION: (how to avoid this class of failure)
"""


def build_self_healing_prompt(failed_locator: str, available_elements: str) -> str:
    return f"""You are an AI-powered Selenium self-healing engine.

A test failed because this locator no longer matches any element:
  FAILED LOCATOR: {failed_locator}

Here are the elements currently present in the DOM:
{available_elements}

Respond with:
1. RECOMMENDED LOCATOR: (e.g. By.CSS_SELECTOR, "button[data-testid='login-submit']")
2. CONFIDENCE: High / Medium / Low
3. REASONING: (one sentence explaining why this is the best match)
4. ALTERNATIVE: (a second option if confidence is not High)
"""


def build_failure_analysis_prompt(test_name: str, error: str, screenshot_path: str = "") -> str:
    """Used by utils/ai/failure_analysis.py for post-run analysis."""
    screenshot_note = f"\nScreenshot saved at: {screenshot_path}" if screenshot_path else ""
    return f"""You are a QA engineer reviewing an automated test failure.

TEST NAME: {test_name}
ERROR: {error}{screenshot_note}

Provide:
1. LIKELY CAUSE:
2. SUGGESTED FIX:
3. IS THIS FLAKY?: Yes / No / Maybe
"""