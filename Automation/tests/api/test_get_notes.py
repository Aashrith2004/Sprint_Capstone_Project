import allure

from api.auth_api import AuthAPI
from api.notes_api import NotesAPI
from config.environment import config


@allure.feature("Notes API")
@allure.story("GET Notes API")
class TestGetNotesAPI:

    @allure.title(
        "TC-API-02 | Verify GET /notes"
    )
    def test_get_notes(self):

        auth_api = AuthAPI()

        token = auth_api.get_token(
            config.credentials.email,
            config.credentials.password,
        )

        notes_api = NotesAPI()

        response = notes_api.get_notes(
            token
        )

        # Status validation
        assert response.status_code == 200

        
        response_data = response.json()

        assert "data" in response_data

        assert isinstance(
            response_data["data"],
            list
        )

       
