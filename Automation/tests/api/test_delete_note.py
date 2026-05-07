import time
import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Notes API")
@allure.story("Delete Note API")
class TestDeleteNoteAPI:

    @allure.title(
        "TC-API-04 | Verify Delete Note API"
    )
    def test_delete_note_api(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        # Create note first
        note_title = (
            f"Delete API {int(time.time())}"
        )

        create_response = (
            notes_api.create_note(
                token=token,
                title=note_title,
                description="Delete API Test",
                category="Home",
            )
        )

        assert create_response.status_code == 200

        note_id = (
            create_response
            .json()["data"]["id"]
        )

        # Delete note
        delete_response = (
            notes_api.delete_note(
                token=token,
                note_id=note_id,
            )
        )

        # Status validation
        assert delete_response.status_code == 200


        # Verify note removed
        get_response = notes_api.get_notes(
            token
        )

        notes = (
            get_response
            .json()["data"]
        )

        deleted_note = [

            note for note in notes

            if note["id"] == note_id
        ]

        assert len(deleted_note) == 0

        
