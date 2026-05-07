import time
import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Notes API")
@allure.story("GET Note By ID After Delete")
class TestGetNoteByIDPostDelete:

    @allure.title(
        "TC-API-05 | Verify deleted note "
        "cannot be fetched by ID"
    )
    def test_get_note_by_id_post_delete(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        # ─────────────────────────────────────
        # Create Note
        # ─────────────────────────────────────

        note_title = (
            f"Delete Validation {int(time.time())}"
        )

        create_response = (
            notes_api.create_note(
                token=token,
                title=note_title,
                description="Post delete validation",
                category="Home",
            )
        )

        assert create_response.status_code == 200

        note_id = (
            create_response
            .json()["data"]["id"]
        )

        # ─────────────────────────────────────
        # Delete Note
        # ─────────────────────────────────────

        delete_response = (
            notes_api.delete_note(
                token=token,
                note_id=note_id,
            )
        )

        assert delete_response.status_code == 200

        # ─────────────────────────────────────
        # GET Note By ID
        # ─────────────────────────────────────

        get_response = (
            notes_api.get_note_by_id(
                token=token,
                note_id=note_id,
            )
        )

        # ─────────────────────────────────────
        # Validations
        # ─────────────────────────────────────

        assert get_response.status_code == 404

        response_data = (
            get_response.json()
        )

        assert (
            response_data["success"]
            is False
        )
