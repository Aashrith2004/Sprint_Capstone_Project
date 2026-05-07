"""
tests/ui/test_login.py

UI test cases for Login functionality.
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
@pytest.mark.ui
class TestLogin:
    """
    Login test suite.
    """

    @allure.story("Successful Login")
    @allure.title(
        "TC-UI-01: Valid login redirects user to dashboard"
    )
    @allure.severity(
        allure.severity_level.BLOCKER
    )
    def test_valid_login_redirects_to_dashboard(
        self,
        driver,
    ):
        """
        Verify valid login works successfully.
        """

        login_page = LoginPage(driver)

        with allure.step(
            "Login using valid credentials"
        ):

            login_page.login(
                config.credentials.email,
                config.credentials.password,
            )

        with allure.step(
            "Wait for dashboard URL"
        ):

            wait_for_url_contains(
                driver,
                "/notes/app",
                timeout=20,
            )

        with allure.step(
            "Validate home page is displayed"
        ):

            assert (
                login_page.is_home_page_displayed()
            ), (
                "Home page was not displayed "
                "after successful login"
            )

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-01: Invalid password shows error"
    )
    @allure.severity(
        allure.severity_level.CRITICAL
    )
    def test_invalid_password_shows_error(
        self,
        driver,
    ):
        """
        Verify invalid password shows error.
        """

        login_page = LoginPage(driver)

        with allure.step(
            "Attempt login using invalid password"
        ):

            login_page.login(
                config.credentials.email,
                "WrongPassword123!",
            )

        with allure.step(
            "Validate login error is displayed"
        ):

            assert (
                login_page.is_login_error_displayed()
            ), (
                "Expected login error message "
                "for invalid password"
            )

        with allure.step(
            "Validate error message content"
        ):

            error_message = (
                login_page.get_error_message()
            )

            assert (
                error_message.strip() != ""
            ), (
                "Login error message text "
                "was empty"
            )

    @allure.story("Negative Login")
    @allure.title(
        "TC-NEG-02: Invalid email format"
    )
    @allure.severity(
        allure.severity_level.NORMAL
    )
    def test_invalid_email_format(
        self,
        driver,
    ):
        """
        Verify malformed email is rejected.
        """

        login_page = LoginPage(driver)

        with allure.step(
            "Attempt login using invalid email"
        ):

            login_page.login(
                "invalid-email",
                config.credentials.password,
            )

        with allure.step(
            "Validate invalid email handling"
        ):

            assert (
                login_page.is_login_error_displayed()
                or "login" in driver.current_url.lower()
            ), (
                "Invalid email format "
                "was unexpectedly accepted"
            )
