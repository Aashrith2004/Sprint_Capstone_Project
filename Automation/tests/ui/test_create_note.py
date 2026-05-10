"""
tests/ui/notes/test_create_note.py
"""

import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Notes Management")
@pytest.mark.ui
class TestCreateNote:

    @pytest.mark.parametrize(
        "category,description_prefix,scenario_id",
        [
            (
                "Home",
                "Home category note",
                "SC-007"
            ),

            (
                "Work",
                "Work category note",
                "SC-008"
            ),

            (
                "Personal",
                "Personal category note",
                "SC-009"
            ),
        ]
    )
    @allure.story(
        "Create Note With Categories"
    )
    @allure.title(
        "Verify note creation with {category} category"
    )
    def test_create_note_by_category(
        self,
        driver,
        category,
        description_prefix,
        scenario_id,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"{category} Note "
            f"{int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            description_prefix,
            category=category,
        )

        assert (
            notes_page.is_note_present(
                note_title
            )
        ), (
            f"{scenario_id}: "
            f"Note creation failed for "
            f"{category} category"
        )