"""
app.py  —  AI QA Test Generation Agent  (Streamlit UI)
Run: streamlit run app.py
"""

import streamlit as st
from agents.test_generation_agent import TestGenerationAgent
from agents.flaky_analyzer_agent import FlakyAnalyzerAgent
from agents.self_healing_agent import SelfHealingAgent
from tools.file_writer import save_test_file

# ── sample data matching your project's real failures ──────────────────────
SAMPLE_FAILURE = {
    "failed_locator": 'By.ID, "login-btn"',
    "error_message": (
        "selenium.common.exceptions.NoSuchElementException: "
        'Unable to locate element: {"method":"css selector","selector":"#login-btn"}\n'
        "  at tests/ui/test_valid_login.py:34 in test_valid_login\n"
        "  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'login-btn')))"
    ),
    "available_dom": (
        '<button id="btn-login" class="login-button" data-testid="login-submit">Login</button>\n'
        '<input id="email-field" name="email" type="email" />\n'
        '<input id="password-field" name="password" type="password" />\n'
        '<a href="/forgot-password" class="forgot-link">Forgot Password?</a>'
    ),
}

# ── page config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="AI QA Agent — Notes App", layout="wide")
st.title("🤖 AI-Powered QA Test Generation Agent")
st.markdown("Generate **pytest + Selenium** automation scripts for the **Notes App** using AI.")

tab1, tab2 = st.tabs(["⚡ Test Generator", "🩺 Flaky Test Healer"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — TEST GENERATOR
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("Generate Automation Script from Requirement")

    requirement = st.text_area(
        "Enter Testing Requirement",
        height=220,
        placeholder=(
            "Example:\n"
            "Test the Create Note page.\n\n"
            "Test Cases:\n"
            "- Valid note creation\n"
            "- Empty title validation\n"
            "- Empty description validation\n"
            "- Note appears in list after creation"
        ),
    )

    col1, col2 = st.columns([1, 3])
    with col1:
        generate_clicked = st.button("⚡ Generate Test", use_container_width=True)

    if generate_clicked:
        if not requirement.strip():
            st.warning("Please enter a testing requirement first.")
        else:
            with st.spinner("AI Agent generating test script..."):
                agent = TestGenerationAgent()
                generated = agent.generate_test(requirement)

            st.subheader("Generated Automation Script")
            st.code(generated, language="python")

            file_path = save_test_file(generated)
            st.success(f"✅ Test saved to: `{file_path}`")

            st.download_button(
                "⬇ Download .py",
                data=generated,
                file_name="test_ai_generated.py",
                mime="text/x-python",
            )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FLAKY TEST HEALER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("AI-Powered Flaky Test Analysis & Self-Healing")
    st.markdown(
        "Simulates a real failure from your **tests/ui/test_valid_login.py** "
        "and uses two agents to diagnose and heal it."
    )

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Simulated Error**")
        st.code(SAMPLE_FAILURE["error_message"], language="text")
    with col_b:
        st.markdown("**Current DOM Elements**")
        st.code(SAMPLE_FAILURE["available_dom"], language="html")
        st.caption(f"Failed locator: `{SAMPLE_FAILURE['failed_locator']}`")

    if st.button("🩺 Analyze & Self-Heal", use_container_width=False):
        with st.spinner("Step 1 — FlakyAnalyzerAgent analyzing failure..."):
            flaky_agent = FlakyAnalyzerAgent()
            analysis = flaky_agent.analyze_failure(SAMPLE_FAILURE["error_message"])

        st.subheader("🔍 Flaky Test Analysis")
        st.write(analysis)

        with st.spinner("Step 2 — SelfHealingAgent recovering locator..."):
            healing_agent = SelfHealingAgent()
            healing = healing_agent.heal_locator(
                SAMPLE_FAILURE["failed_locator"],
                SAMPLE_FAILURE["available_dom"],
            )

        st.subheader("✨ Self-Healing Recommendation")
        st.write(healing)

        st.success("✅ Both agents finished. Update your page object with the recommended locator.")