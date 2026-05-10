"""
tests/ai/test_ai_generated_note.py
"""

import allure

from pages.login_page import LoginPage

from pages.notes_page import (
    NotesPage,
)

from utils.llm.llm_helper import (
    generate_note_data
)

from utils.llm.failure_analysis import (
    analyze_failure
)


@allure.feature("AI + MCP")
@allure.story(
    "LLM-powered test data generation"
)
class TestAIGeneratedNote:

    def test_create_note_using_ai_data(
        self,
        driver
    ):

        try:

            # Login

            login_page = LoginPage(driver)

            login_page.login_with_defaults()

            note_data = generate_note_data()

            title = note_data["title"]

            description = note_data[
                "description"
            ]

            notes_page = (
                NotesPage(driver)
            )

            notes_page.create_note(
                title=title,
                description=description
            )

            assert (
                notes_page
                .is_note_present(title)
            )

        except Exception as e:

            suggestion = analyze_failure(
                str(e)
            )

            print(suggestion)

            raise