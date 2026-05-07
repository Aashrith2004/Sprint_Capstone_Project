"""
fixtures/browser_fixture.py
"""

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def create_driver(
    browser_name: str = "chrome"
) -> WebDriver:
    """
    Create Chrome WebDriver safely.
    """

    logger.info(
        f"Launching browser: {browser_name}"
    )

    options = webdriver.ChromeOptions()

    # Headless mode
    if config.browser.headless:

        options.add_argument(
            "--headless=new"
        )

    # Stability arguments
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
        "--remote-allow-origins=*"
    )

    options.add_argument(
        "--disable-extensions"
    )

    options.add_argument(
        "--start-maximized"
    )

    service = Service(
        ChromeDriverManager().install()
    )

    if config.execution_type == "local":

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

    else:

        driver = webdriver.Remote(
            command_executor=config.remote_url,
            options=options
        )

    logger.info(
        "Browser launched successfully"
    )

    return driver


def quit_driver(
    driver: WebDriver
) -> None:
    """
    Close browser safely.
    """

    if driver:

        logger.info(
            "Closing browser"
        )

        try:

            driver.quit()

            logger.info(
                "Browser closed successfully"
            )

        except Exception as e:

            logger.error(
                f"Error closing browser: {e}"
            )

        finally:

            driver = None