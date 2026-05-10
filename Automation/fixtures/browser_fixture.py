"""
fixtures/browser_fixture.py
"""

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver

from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(
    browser_name: str = "chrome"
) -> WebDriver:
    """
    Create browser driver dynamically.
    """

    logger.info(
        f"Launching browser: {browser_name}"
    )

    browser_name = browser_name.lower()

    # ==================================================
    # CHROME
    # ==================================================

    if browser_name == "chrome":

        options = webdriver.ChromeOptions()

        if config.browser.headless:

            options.add_argument(
                "--headless=new"
            )

        options.add_argument(
            "--window-size=1920,1080"
        )

        options.add_argument(
            "--disable-dev-shm-usage"
        )

        options.add_argument(
            "--no-sandbox"
        )

        options.add_argument(
            "--disable-gpu"
        )

        options.add_argument(
            "--disable-notifications"
        )

        options.add_argument(
            "--disable-popup-blocking"
        )

        options.add_argument(
            "--disable-extensions"
        )

        options.add_argument(
            "--start-maximized"
        )

        # Local execution
        if config.execution_type == "local":

            driver = webdriver.Chrome(
                options=options
            )

        # Remote execution
        else:

            driver = webdriver.Remote(
                command_executor=config.remote_url,
                options=options
            )

    # ==================================================
    # FIREFOX
    # ==================================================

    elif browser_name == "firefox":

        options = webdriver.FirefoxOptions()

        if config.browser.headless:

            options.add_argument(
                "--headless"
            )

        options.add_argument(
            "--width=1920"
        )

        options.add_argument(
            "--height=1080"
        )

        # Local execution
        if config.execution_type == "local":

            driver = webdriver.Firefox(
                options=options
            )

        # Remote execution
        else:

            driver = webdriver.Remote(
                command_executor=config.remote_url,
                options=options
            )

    else:

        raise ValueError(
            f"Unsupported browser: {browser_name}"
        )

    logger.info(
        f"{browser_name} browser launched successfully"
    )

    return driver


def quit_driver(driver: WebDriver) -> None:
    """
    Close browser safely.
    """

    if driver:

        logger.info(
            "Closing browser"
        )

        try:

            driver.close()

        except Exception as e:

            logger.warning(
                f"Driver close failed: {e}"
            )

        try:

            driver.quit()

            logger.info(
                "Browser closed successfully"
            )

        except Exception as e:

            logger.warning(
                f"Driver quit failed: {e}"
            )