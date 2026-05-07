import json
import requests
import allure

from config.environment import config


class APIClient:

    def __init__(self):

        self.base_url = (
            config.app.api_base_url
        )

        self.timeout = (
            config.timeouts.api_timeout
        )

        self.session = requests.Session()

    def post(
        self,
        endpoint,
        payload=None,
        headers=None,
    ):

        url = f"{self.base_url}{endpoint}"

        response = self.session.post(
            url,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )

        # Attach Request
        allure.attach(
            json.dumps(payload, indent=4),
            name="POST Request Payload",
            attachment_type=allure.attachment_type.JSON
        )

        # Attach Response
        allure.attach(
            response.text,
            name="POST Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response

    def get(
        self,
        endpoint,
        headers=None,
    ):

        url = f"{self.base_url}{endpoint}"

        response = self.session.get(
            url,
            headers=headers,
            timeout=self.timeout,
        )

        # Attach Response
        allure.attach(
            response.text,
            name="GET Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response

    def delete(
        self,
        endpoint,
        headers=None,
    ):

        url = f"{self.base_url}{endpoint}"

        response = self.session.delete(
            url,
            headers=headers,
            timeout=self.timeout,
        )

        # Attach Response
        allure.attach(
            response.text,
            name="DELETE Response",
            attachment_type=allure.attachment_type.JSON
        )

        return response