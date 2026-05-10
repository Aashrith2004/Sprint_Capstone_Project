"""
tests/ui/notes/test_delete_note.py
"""

import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Delete Note")
@pytest.mark.ui
class TestDeleteNote:

    @pytest.mark.smoke
    @allure.story("Delete Note")
    @allure.title(
        "SC-014: Verify note deletion"
    )
    def test_create_and_delete_note(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"Delete Note "
            f"{int(time.time())}"
        )

        notes_page.create_note(
            note_title,
            "Delete note validation",
            category="Home",
        )

        assert (
            notes_page.is_note_present(
                note_title
            )
        ), (
            f"Created note "
            f"'{note_title}' "
            f"was not found"
        )

        notes_page.delete_note()

        notes_page.confirm_delete()

        assert (
            notes_page.wait_for_note_gone(
                note_title
            )
        ), (
            f"Note '{note_title}' "
            "still visible after deletion"
        )