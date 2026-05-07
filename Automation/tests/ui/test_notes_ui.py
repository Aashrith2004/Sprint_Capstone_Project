"""
tests/ui/test_notes_ui.py

UI tests for Notes functionality.
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
class TestNotesUI:
    """
    Notes UI test suite.
    """

    @pytest.mark.parametrize(
        "category,description_prefix,scenario_id",
        [
            ("Home", "Home category note", "SC-007"),
            ("Work", "Work category note", "SC-008"),
            ("Personal", "Personal category note", "SC-009"),
        ]
    )
    @allure.story("Create Note With Categories")
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
        """
        Verify note can be created
        with different categories.
        """

        login_page = LoginPage(driver)

        with allure.step(
            "Login to application"
        ):

            login_page.login(
                config.credentials.email,
                config.credentials.password,
            )

        notes_page = NotesPage(driver)

        note_title = (
            f"{category} Note {int(time.time())}"
        )

        with allure.step(
            f"Create note in {category} category"
        ):

            notes_page.create_note(
                note_title,
                description_prefix,
                category=category,
            )

        with allure.step(
            "Validate note is displayed"
        ):

            assert (
                notes_page.is_note_present(
                    note_title
                )
            ), (
                f"{scenario_id}: "
                f"Note creation failed for "
                f"{category} category"
            )

    @allure.story("Empty Title Validation")
    @allure.title(
        "SC-012: Verify validation for empty title"
    )
    def test_create_note_empty_title(
        self,
        driver,
    ):
        """
        Verify validation appears
        when title is empty.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        with allure.step(
            "Open Add Note form"
        ):

            notes_page.click_add_note()

        with allure.step(
            "Enter description only"
        ):

            notes_page.enter_description(
                "Description without title"
            )

        with allure.step(
            "Select category"
        ):

            notes_page.select_category(
                "Home"
            )

        with allure.step(
            "Click Save"
        ):

            notes_page.click_save()

        with allure.step(
            "Validate title required error"
        ):

            assert (
                notes_page.is_title_required_error_displayed()
            ), (
                "Title required validation "
                "message not displayed"
            )

    @allure.story("Empty Description Validation")
    @allure.title(
        "SC-013: Verify validation for empty description"
    )
    def test_create_note_empty_description(
        self,
        driver,
    ):
        """
        Verify validation appears
        when description is empty.
        """

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        note_title = (
            f"No Description {int(time.time())}"
        )

        with allure.step(
            "Open Add Note form"
        ):

            notes_page.click_add_note()

        with allure.step(
            "Enter title only"
        ):

            notes_page.enter_title(
                note_title
            )

        with allure.step(
            "Select category"
        ):

            notes_page.select_category(
                "Home"
            )

        with allure.step(
            "Click Save"
        ):

            notes_page.click_save()

        with allure.step(
            "Validate description required error"
        ):

            assert (
                notes_page.is_description_required_error_displayed()
            ), (
                "Description required validation "
                "message not displayed"
            )

    @pytest.mark.smoke
    @allure.story("Delete Note")
    @allure.title(
        "SC-014: Verify note deletion"
    )
    def test_create_and_delete_note(
        self,
        driver,
    ):
        """
        Verify created note
        can be deleted successfully.
        """

        login_page = LoginPage(driver)

        with allure.step(
            "Login to application"
        ):

            login_page.login(
                config.credentials.email,
                config.credentials.password,
            )

        notes_page = NotesPage(driver)

        note_title = (
            f"Delete Note {int(time.time())}"
        )

        with allure.step(
            "Create note"
        ):

            notes_page.create_note(
                note_title,
                "Delete note validation",
                category="Home",
            )

        with allure.step(
            "Verify note created"
        ):

            assert (
                notes_page.is_note_present(
                    note_title
                )
            ), (
                f"Created note "
                f"'{note_title}' "
                f"was not found"
            )

        with allure.step(
            "Delete note"
        ):

            notes_page.delete_note()

        with allure.step(
            "Confirm delete"
        ):

            notes_page.confirm_delete()

        with allure.step(
            "Validate note removed"
        ):

            assert (
                notes_page.wait_for_note_gone(
                    note_title
                )
            ), (
                f"Note '{note_title}' "
                "still visible after deletion"
            )
