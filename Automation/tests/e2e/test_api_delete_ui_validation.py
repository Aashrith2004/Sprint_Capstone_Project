import time
import allure

from pages.login_page import LoginPage
from pages.notes_page import NotesPage

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI

from config.environment import config


@allure.epic("Hybrid E2E")
@allure.feature("API Delete → UI Validation")
class TestAPIDeleteUIValidation:

    @allure.title(
        "TC-E2E-02 | Verify API deleted note disappears from UI"
    )
    def test_api_delete_reflects_in_ui(
        self,
        driver,
    ):

        # ─────────────────────────────────────
        # UI Login
        # ─────────────────────────────────────

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        notes_page = NotesPage(driver)

        # ─────────────────────────────────────
        # API Login
        # ─────────────────────────────────────

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        # ─────────────────────────────────────
        # Create Note via API
        # ─────────────────────────────────────

        note_title = (
            f"API Delete {int(time.time())}"
        )

        create_response = (
            notes_api.create_note(
                token=token,
                title=note_title,
                description="Delete via API",
                category="Home",
            )
        )

        assert create_response.status_code == 200

        note_id = (
            create_response
            .json()["data"]["id"]
        )

        # Refresh UI to load note
        notes_page.refresh_notes_page()

        # Validate note visible in UI
        assert notes_page.is_note_present(
            note_title
        )

        # ─────────────────────────────────────
        # Delete Note via API
        # ─────────────────────────────────────

        delete_response = (
            notes_api.delete_note(
                token=token,
                note_id=note_id,
            )
        )

        assert delete_response.status_code == 200

        # ─────────────────────────────────────
        # Refresh UI
        # ─────────────────────────────────────

        notes_page.refresh_notes_page()

        # ─────────────────────────────────────
        # Validate note removed from UI
        # ─────────────────────────────────────

        assert not notes_page.is_note_present(
            note_title,
            timeout=5,
        ), (
            "Deleted API note still visible in UI"
        )