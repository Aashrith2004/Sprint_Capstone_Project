"""
conftest.py
"""

from pathlib import Path
import os
import time
import allure
import pytest

from config.environment import (
    config as framework_config
)

from fixtures.browser_fixture import (
    create_driver,
    quit_driver,
)


def pytest_configure(config):
    """
    Create report folders.
    """

    Path(
        framework_config.reporting.allure_results_dir
    ).mkdir(
        parents=True,
        exist_ok=True,
    )

    Path(
        "reports/screenshots"
    ).mkdir(
        parents=True,
        exist_ok=True,
    )


@pytest.fixture(scope="function")
def driver():
    """
    Create browser instance.
    """

    drv = create_driver()

    drv.set_window_size(
        1920,
        1080
    )

    drv.implicitly_wait(3)

    yield drv

    try: quit_driver(drv); 
    except Exception as e: print(f"Driver cleanup failed: {e}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call,
):
    """
    Capture screenshot on failure.
    """

    outcome = yield

    report = outcome.get_result()

    if (
        report.when == "call"
        and report.failed
    ):

        driver = item.funcargs.get(
            "driver"
        )

        if driver:

            timestamp = int(time.time())

            screenshot_path = (
                f"reports/screenshots/"
                f"{item.name}_{timestamp}.png"
            )

            try:

                driver.save_screenshot(
                    screenshot_path
                )

                allure.attach.file(
                    screenshot_path,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            except Exception as e:

                print(
                    f"Screenshot failed: {e}"
                )
