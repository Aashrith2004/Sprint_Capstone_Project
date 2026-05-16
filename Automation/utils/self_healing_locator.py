"""
utils/self_healing_locator.py

Self-healing locator utility.
Attempts multiple locators until one succeeds.
"""

from selenium.common.exceptions import NoSuchElementException

from utils.logger import get_logger

logger = get_logger(__name__)


def find_element_with_fallback(driver, locators):

    for locator in locators:

        try:

            element = driver.find_element(*locator)

            logger.info(f"Locator succeeded: {locator}")

            return element

        except Exception:

            logger.warning(f"Locator failed: {locator}")

    raise NoSuchElementException(
        f"All locators failed: {locators}"
    )