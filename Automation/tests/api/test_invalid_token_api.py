import allure

from api.notes_api import NotesAPI


@allure.feature("Negative API")
@allure.story("Invalid Token")
class TestInvalidTokenAPI:

    @allure.title(
        "TC-NEG-API-04 | Invalid token validation"
    )
    def test_invalid_token(self):

        notes_api = NotesAPI()

        response = notes_api.get_notes(
            "invalid_token"
        )

        assert response.status_code == 401

        response_data = response.json()

        assert response_data["success"] is False