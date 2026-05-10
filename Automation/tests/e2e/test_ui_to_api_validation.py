import time
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI

from config.environment import config


@allure.epic("Hybrid E2E")
@allure.feature("UI to API Validation")
class TestUIToAPIValidation:

    @allure.title(
        "TC-E2E-01 | Verify UI created note exists in API"
    )
    def test_ui_created_note_exists_in_api(
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
            f"Hybrid Note {int(time.time())}"
        )

        note_description = (
            "Created via UI"
        )

        notes_page.create_note(
            title=note_title,
            description=note_description,
            category="Home",
        )

        assert notes_page.is_note_present(
            note_title
        )

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )
        notes_api = NotesAPI()
        response = notes_api.get_notes(
            token
        )
        assert response.status_code == 200
        notes = (
            response.json()["data"]
        )
        matching_notes = [
            note for note in notes
            if (
                note["title"] == note_title
                and
                note["description"] == note_description
            )
        ]
        assert len(matching_notes) > 0, (
            "UI created note "
            "not found in API response"
        )