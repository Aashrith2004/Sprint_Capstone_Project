import time
import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Negative API")
@allure.story("Empty Description Validation")
class TestCreateNoteEmptyDescription:

    @allure.title(
        "TC-NEG-API-03 | Empty description"
    )
    def test_create_note_empty_description(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        response = notes_api.create_note(
            token=token,
            title=f"API {int(time.time())}",
            description="",
            category="Home",
        )

        assert response.status_code == 400

        response_data = response.json()

        assert response_data["success"] is False