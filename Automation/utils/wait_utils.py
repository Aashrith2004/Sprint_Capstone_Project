"""
utils/wait_utils.py
Custom intelligent wait utilities wrapping Selenium's WebDriverWait.
Provides cleaner, reusable wait methods with logging and error handling.
"""

import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException,
    NoSuchElementException,
    ElementNotInteractableException,
)
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = config.timeouts.explicit_wait
POLL_FREQUENCY = 0.5  


def wait_for_element_visible(
    driver: WebDriver,
    locator: tuple,
    timeout: int = DEFAULT_TIMEOUT,
) -> WebElement:
    
    logger.debug(f"Waiting for visible element: {locator}")
    try:
        return WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.visibility_of_element_located(locator)
        )
    except TimeoutException:
        logger.error(f"Element not visible after {timeout}s: {locator}")
        raise


def wait_for_element_clickable(
    driver: WebDriver,
    locator: tuple,
    timeout: int = DEFAULT_TIMEOUT,
) -> WebElement:
    """
    Waits until element is visible and enabled (ready to click).
    """
    logger.debug(f"Waiting for clickable element: {locator}")
    try:
        return WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.element_to_be_clickable(locator)
        )
    except TimeoutException:
        logger.error(f"Element not clickable after {timeout}s: {locator}")
        raise


def wait_for_text_in_element(
    driver: WebDriver,
    locator: tuple,
    text: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    logger.debug(f"Waiting for text '{text}' in element: {locator}")
    try:
        return WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.text_to_be_present_in_element(locator, text)
        )
    except TimeoutException:
        logger.error(f"Text '{text}' not found in {locator} after {timeout}s")
        raise


def wait_for_element_to_disappear(
    driver: WebDriver,
    locator: tuple,
    timeout: int = DEFAULT_TIMEOUT,) -> bool:
    logger.debug(f"Waiting for element to disappear: {locator}")
    try:
        return WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.invisibility_of_element_located(locator)
        )
    except TimeoutException:
        logger.error(f"Element still visible after {timeout}s: {locator}")
        raise


def wait_for_url_contains(
    driver: WebDriver,
    partial_url: str,
    timeout: int = DEFAULT_TIMEOUT,
) -> bool:
    """
    Waits until the browser URL contains the specified substring.
    """
    logger.debug(f"Waiting for URL to contain: '{partial_url}'")
    try:
        return WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            EC.url_contains(partial_url)
        )
    except TimeoutException:
        logger.error(f"URL did not contain '{partial_url}' after {timeout}s")
        raise


def wait_for_page_ready(driver: WebDriver, timeout: int = DEFAULT_TIMEOUT) -> None:
    
    logger.debug("Waiting for page readyState == complete")
    try:
        WebDriverWait(driver, timeout, poll_frequency=POLL_FREQUENCY).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
    except TimeoutException:
        logger.error(f"Page not ready after {timeout}s")
        raise


def retry_click(
    driver: WebDriver,
    locator: tuple,
    max_attempts: int = config.timeouts.retry_attempts,
    delay: float = config.timeouts.retry_delay,
) -> None:
    
    for attempt in range(1, max_attempts + 1):
        try:
            element = wait_for_element_clickable(driver, locator)
            element.click()
            logger.debug(f"Click succeeded on attempt {attempt}: {locator}")
            return
        except (StaleElementReferenceException, ElementNotInteractableException) as exc:
            logger.warning(f"Click attempt {attempt} failed ({type(exc).__name__}): {locator}")
            if attempt == max_attempts:
                raise
            time.sleep(delay)


def safe_send_keys(
    driver: WebDriver,
    locator: tuple,
    text: str,
    clear_first: bool = True,
) -> None:
    """
    Waits for an input element, optionally clears it, then types the given text.
    """
    element = wait_for_element_visible(driver, locator)
    if clear_first:
        element.clear()
    element.send_keys(text)
    logger.debug(f"Sent keys to {locator}: '{text}'")
