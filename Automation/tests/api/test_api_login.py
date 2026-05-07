import allure

from api.auth_api import AuthAPI
from config.environment import config


@allure.feature("Notes API")
@allure.story("Login API")
class TestAPILogin:

    @allure.title(
        "TC-API-01 | Verify API Login"
    )
    def test_api_login(self):

        auth_api = AuthAPI()

        response = auth_api.login(
            config.credentials.email,
            config.credentials.password,
        )

        assert response.status_code == 200

        response_data = response.json()

        assert "token" in response_data["data"]