"""
pages/login_page.py

Page Object for the ExpandTesting Notes login page.
"""

import time
import allure

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from config.environment import config
from utils.logger import get_logger
from utils.self_healing_locator import (
    find_element_with_fallback,
)

logger = get_logger(__name__)


class LoginPage(BasePage):
    URL = config.app.ui_base_url

    _LANDING_LOGIN_BUTTON = [
        (
            By.CSS_SELECTOR,
            "a[href='/notes/app/login']",
        ),
        (
            By.XPATH,
            "//a[contains(text(),'Login')]",
        ),
    ]

    _EMAIL_INPUT = [
        (
            By.ID,
            "email"
        ),
        (
            By.CSS_SELECTOR,
            "input[type='email']"
        ),
        (
            By.XPATH,
            "//input[@placeholder='Email address']",
        ),
    ]

    _PASSWORD_INPUT = [
        (
            By.ID,
            "password"
        ),
        (
            By.CSS_SELECTOR,
            "input[type='password']"
        ),
        (
            By.XPATH,
            "//input[@placeholder='Password']",
        ),
    ]

    _LOGIN_BUTTON = [
        (
            By.CSS_SELECTOR,
            "button[type='submit']",
        ),
        (
            By.XPATH,
            "//button[normalize-space()='Login']",
        ),
    ]

    _HOME_LOGO = (
        By.CSS_SELECTOR,
        "a[data-testid='home']"
    )

    _ERROR_ALERT = (
        By.CSS_SELECTOR,
        "div[data-testid='alert-message']",
    )

    def __init__(self, driver: WebDriver):

        super().__init__(driver)

    def safe_click(self, locator_list, timeout=20):
        """
        Stable click helper for Jenkins/Docker/headless.
        """

        last_exception = None

        for _ in range(3):

            try:

                element = find_element_with_fallback(
                    self.driver,
                    locator_list,
                )

                WebDriverWait(
                    self.driver,
                    timeout
                ).until(
                    EC.visibility_of(element)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});",
                    element
                )

                WebDriverWait(
                    self.driver,
                    timeout
                ).until(
                    lambda d: element.is_enabled()
                )

                try:
                    element.click()

                except Exception:
                    self.driver.execute_script(
                        "arguments[0].click();",
                        element
                    )

                return

            except (
                ElementClickInterceptedException,
                StaleElementReferenceException,
            ) as e:

                last_exception = e
                time.sleep(1)

        raise last_exception

    # ─────────────────────────────────────────────────────────────

    @allure.step("Open Login page")
    def open_login_page(self) -> None:

        self.open(self.URL)

        logger.info(
            "Application landing page opened"
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        self.safe_click(
            self._LANDING_LOGIN_BUTTON
        )

        logger.info(
            "Landing page Login button clicked"
        )

    @allure.step("Enter email")
    def enter_email(
        self,
        email: str
    ) -> None:

        element = find_element_with_fallback(
            self.driver,
            self._EMAIL_INPUT,
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of(element)
        )

        element.clear()

        element.send_keys(email)

        logger.info(
            f"Email entered: {email}"
        )

    @allure.step("Enter password")
    def enter_password(
        self,
        password: str
    ) -> None:

        element = find_element_with_fallback(
            self.driver,
            self._PASSWORD_INPUT,
        )

        WebDriverWait(
            self.driver,
            20
        ).until(
            EC.visibility_of(element)
        )

        element.clear()

        element.send_keys(password)

        logger.info(
            "Password entered"
        )

    @allure.step("Click Login button")
    def click_login(self) -> None:

        self.safe_click(
            self._LOGIN_BUTTON
        )

        logger.info(
            "Login button clicked"
        )

    @allure.step("Perform login")
    def login(
        self,
        email: str,
        password: str,
    ) -> None:

        self.open_login_page()

        self.enter_email(email)

        self.enter_password(password)

        self.click_login()

        logger.info(
            f"Login submitted for user: {email}"
        )

    def login_with_defaults(self) -> None:

        self.login(
            config.credentials.email,
            config.credentials.password,
        )

    # ─────────────────────────────────────────────────────────────
    # Validations
    # ─────────────────────────────────────────────────────────────

    def get_error_message(self) -> str:

        if self.is_visible(
            self._ERROR_ALERT,
            timeout=10,
        ):

            return self.get_text(
                self._ERROR_ALERT
            )

        return ""

    def is_login_error_displayed(self) -> bool:

        return self.is_visible(
            self._ERROR_ALERT,
            timeout=10,
        )

    def is_logged_in(self) -> bool:

        return (
            "/notes/app" in self.get_current_url()
        )

    def is_home_page_displayed(self) -> bool:

        return self.is_visible(
            self._HOME_LOGO,
            timeout=20,
        )
