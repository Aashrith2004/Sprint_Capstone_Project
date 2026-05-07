"""
pages/base_page.py

Base Page Object containing reusable browser interaction methods.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from utils.wait_utils import (
    wait_for_element_visible,
)

from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:
    """
    Parent class for all Page Objects.
    """

    def __init__(self, driver: WebDriver):

        self.driver = driver

    def open(self, url: str) -> None:
        """
        Opens the specified URL.
        """

        logger.info(f"Opening URL: {url}")

        self.driver.get(url)

    def find(self, locator: tuple):

        return wait_for_element_visible(
            self.driver,
            locator,
        )

    def click(self, locator: tuple) -> None:

        self.find(locator).click()

    def type(self, locator: tuple, text: str) -> None:

        element = self.find(locator)

        element.clear()

        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:

        return self.find(locator).text

    def is_visible(
        self,
        locator: tuple,
        timeout: int = 5,
    ) -> bool:

        try:
            wait_for_element_visible(
                self.driver,
                locator,
                timeout,
            )
            return True

        except Exception:
            return False

    def get_current_url(self) -> str:

        return self.driver.current_url