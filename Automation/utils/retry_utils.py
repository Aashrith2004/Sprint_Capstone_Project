"""
utils/retry_utils.py
Retry mechanism for flaky UI/API actions.
Provides both a function-level decorator and a generic retry helper
to handle transient failures (StaleElement, network hiccups, etc.).
"""

import time
import functools
from typing import Callable, Type, Tuple, Any, Optional
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)

# Default exceptions to retry on for Selenium-related flakiness
DEFAULT_SELENIUM_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    StaleElementReferenceException,
    ElementNotInteractableException,
    ElementClickInterceptedException,
    TimeoutException,
    WebDriverException,
)


def retry(
    max_attempts: int = config.timeouts.retry_attempts,
    delay: float = config.timeouts.retry_delay,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_SELENIUM_EXCEPTIONS,
    on_retry: Optional[Callable] = None,
):
    """
    Decorator that retries the wrapped function on specified exceptions.

    Args:
        max_attempts: Total number of attempts (1 = no retry).
        delay:        Seconds to wait between attempts.
        exceptions:   Tuple of exception types that trigger a retry.
        on_retry:     Optional callback(attempt, exc) called before each retry.

    Example:
        @retry(max_attempts=3, delay=1)
        def click_button(driver, locator):
            driver.find_element(*locator).click()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"[RETRY] '{func.__name__}' succeeded on attempt {attempt}")
                    return result
                except exceptions as exc:
                    last_exc = exc
                    logger.warning(
                        f"[RETRY] '{func.__name__}' attempt {attempt}/{max_attempts} "
                        f"failed: {type(exc).__name__}: {exc}"
                    )
                    if on_retry:
                        on_retry(attempt, exc)
                    if attempt < max_attempts:
                        time.sleep(delay)
            # All attempts exhausted
            logger.error(
                f"[RETRY] '{func.__name__}' failed after {max_attempts} attempts"
            )
            raise last_exc
        return wrapper
    return decorator


def retry_action(
    action: Callable,
    max_attempts: int = config.timeouts.retry_attempts,
    delay: float = config.timeouts.retry_delay,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_SELENIUM_EXCEPTIONS,
) -> Any:
    """
    Inline retry wrapper for one-off callable actions (no decorator syntax).

    Args:
        action:       Zero-argument callable to retry.
        max_attempts: Total attempts.
        delay:        Seconds between attempts.
        exceptions:   Exception types that trigger retry.

    Returns:
        Return value of the action on success.

    Example:
        result = retry_action(lambda: driver.find_element(By.ID, "btn").click())
    """
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            return action()
        except exceptions as exc:
            last_exc = exc
            logger.warning(
                f"[RETRY] Inline action attempt {attempt}/{max_attempts}: "
                f"{type(exc).__name__}"
            )
            if attempt < max_attempts:
                time.sleep(delay)
    raise last_exc


def wait_and_retry(
    condition: Callable[[], bool],
    max_attempts: int = 5,
    delay: float = 0.5,
    label: str = "condition",
) -> bool:
    """
    Polls a boolean-returning callable until it returns True or attempts are exhausted.
    Useful for assertions that may take a moment to stabilise (e.g. DOM updates).

    Args:
        condition:    Callable returning True when ready.
        max_attempts: Number of polls before giving up.
        delay:        Seconds between polls.
        label:        Human-readable name logged on each attempt.

    Returns:
        True if condition met, False if exhausted.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            if condition():
                logger.debug(f"[WAIT-RETRY] '{label}' met on attempt {attempt}")
                return True
        except Exception as exc:
            logger.debug(f"[WAIT-RETRY] '{label}' attempt {attempt} raised: {exc}")
        if attempt < max_attempts:
            time.sleep(delay)
    logger.warning(f"[WAIT-RETRY] '{label}' not met after {max_attempts} attempts")
    return False
