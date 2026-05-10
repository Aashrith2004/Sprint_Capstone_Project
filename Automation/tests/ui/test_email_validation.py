"""
tests/ui/authentication/test_email_validation.py
"""

import allure
import pytest

from pages.login_page import LoginPage
from config.environment import config


@allure.epic("Notes App Automation")
@allure.feature("UI Authentication")
@pytest.mark.ui
class TestEmailValidation:

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-02: Invalid email format"
    )
    def test_invalid_email_format(
        self,
        driver,
    ):

        login_page = LoginPage(driver)

        login_page.login(
            "invalid-email",
            config.credentials.password,
        )

        assert (
            login_page.is_login_error_displayed()
            or "login"
            in driver.current_url.lower()
        )