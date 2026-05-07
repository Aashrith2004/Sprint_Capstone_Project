from api.api_client import APIClient


class AuthAPI(APIClient):

    def login(
        self,
        email,
        password,
    ):

        payload = {
            "email": email,
            "password": password,
        }

        return self.post(
            "/users/login",
            payload=payload,
        )

    def get_token(
        self,
        email,
        password,
    ):

        response = self.login(
            email,
            password,
        )

        response_data = response.json()

        return response_data["data"]["token"]