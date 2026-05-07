import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Negative API")
@allure.story("Empty Title Validation")
class TestCreateNoteEmptyTitle:

    @allure.title(
        "TC-NEG-API-02 | Create note with empty title"
    )
    def test_create_note_empty_title(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        response = notes_api.create_note(
            token=token,
            title="",
            description="No title",
            category="Home",
        )

        assert response.status_code == 400

        response_data = response.json()

        assert response_data["success"] is False