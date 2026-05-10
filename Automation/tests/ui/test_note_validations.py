"""
tests/ui/notes/test_note_validations.py
"""

import time
import allure
import pytest

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("Notes Validation")
@pytest.mark.ui
class TestNoteValidations:

    @allure.story(
        "Empty Title Validation"
    )
    @allure.title(
        "SC-012: Verify validation for empty title"
    )
    def test_create_note_empty_title(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        notes_page.click_add_note()

        notes_page.enter_description(
            "Description without title"
        )

        notes_page.select_category(
            "Home"
        )

        notes_page.click_save()

        assert (
            notes_page
            .is_title_required_error_displayed()
        ), (
            "Title required validation "
            "message not displayed"
        )

    @allure.story(
        "Empty Description Validation"
    )
    @allure.title(
        "SC-013: Verify validation for empty description"
    )
    def test_create_note_empty_description(
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
            f"No Description "
            f"{int(time.time())}"
        )

        notes_page.click_add_note()

        notes_page.enter_title(
            note_title
        )

        notes_page.select_category(
            "Home"
        )

        notes_page.click_save()

        assert (
            notes_page
            .is_description_required_error_displayed()
        ), (
            "Description required validation "
            "message not displayed"
        )