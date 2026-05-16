"""
utils/screenshot.py
Screenshot capture utility with Allure attachment support.
Called from conftest.py on test failure and manually in test steps.
"""

import allure
import os
from datetime import datetime
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)


def capture_screenshot(driver: WebDriver, name: str = "screenshot") -> str:
    screenshot_dir = Path(config.reporting.screenshot_dir)
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    safe_name = name.replace(" ", "_").replace("/", "-")
    file_path = screenshot_dir / f"{safe_name}_{timestamp}.png"

    try:
        driver.save_screenshot(str(file_path))
        logger.info(f"Screenshot saved → {file_path}")

        # Attach to Allure report as an inline image
        with open(file_path, "rb") as img_file:
            allure.attach(
                img_file.read(),
                name=name,
                attachment_type=allure.attachment_type.PNG,
            )

        return str(file_path)

    except Exception as exc:
        logger.error(f"Failed to capture screenshot '{name}': {exc}")
        return ""
def attach_page_source(driver: WebDriver, name: str = "page_source") -> None:
    """Attaches current page HTML source to Allure report for debugging."""
    try:
        allure.attach(
            driver.page_source,
            name=name,
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:
        logger.warning(f"Could not attach page source: {exc}")
