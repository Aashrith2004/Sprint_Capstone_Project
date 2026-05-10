"""
conftest.py
"""

from pathlib import Path
import time
import allure
import pytest
from utils.screenshot import (
    capture_screenshot,
    attach_page_source,
)
from config.environment import (
    config as framework_config
)

from fixtures.browser_fixture import (
    create_driver,
    quit_driver,
)


def pytest_addoption(parser):
    """
    Add custom browser argument.
    """

    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to execute tests"
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
def driver(request):
    """
    Create browser instance dynamically.
    """
    browser = request.config.getoption(
        "--browser"
    )

    drv = create_driver(browser)

    drv.maximize_window()
    drv.implicitly_wait(3)

    yield drv

    try:

        quit_driver(drv)

    except Exception as e:

        print(
            f"Driver cleanup failed: {e}"
        )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item,
    call,
):

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

            capture_screenshot(
                driver,
                item.name
            )

            attach_page_source(
                driver,
                f"{item.name}_html"
            )