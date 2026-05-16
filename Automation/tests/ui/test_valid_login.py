"""
tests/ui/authentication/test_valid_login.py
"""

import allure
import pytest

from pages.login_page import LoginPage
from config.environment import config

from utils.wait_utils import (
    wait_for_url_contains,
)


@allure.epic("Notes App Automation")
@allure.feature("UI Authentication")
@pytest.mark.empty
class TestValidLogin:

    @allure.story("Successful Login")
    @allure.title(
        "TC-UI-01: Valid login redirects user to dashboard"
    )
    def test_valid_login_redirects_to_dashboard(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            config.credentials.password,
        )

        wait_for_url_contains(
            driver,
            "/notes/app",
            timeout=20,
        )

        assert (
            login_page.is_home_page_displayed()
        )