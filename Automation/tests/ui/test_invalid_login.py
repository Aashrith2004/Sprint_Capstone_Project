"""
tests/ui/authentication/test_invalid_login.py
"""

import allure
import pytest

from pages.login_page import LoginPage
from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("UI Authentication")
@pytest.mark.ui
class TestInvalidLogin:

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-01: Invalid password shows error"
    )
    def test_invalid_password_shows_error(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            config.credentials.email,
            "WrongPassword123!",
        )

        assert (
            login_page.is_login_error_displayed()
        )