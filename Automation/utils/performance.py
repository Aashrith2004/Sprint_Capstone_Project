"""
utils/performance.py
Performance measurement utilities for API response times and UI page load timings.
Logs metrics and attaches them to Allure reports.
"""

import time
import allure
import json
from contextlib import contextmanager
from selenium.webdriver.remote.webdriver import WebDriver
from config.environment import config
from utils.logger import get_logger

logger = get_logger(__name__)

# In-memory store for the session's performance log
_perf_log: list[dict] = []


@contextmanager
def measure_api_time(label: str):
    """
    Context manager that measures elapsed time of an API call block.

    Usage:
        with measure_api_time("GET /notes"):
            response = requests.get(url, headers=headers)

    Logs a warning if the call exceeds the configured threshold.
    """
    start = time.monotonic()
    yield
    elapsed_ms = (time.monotonic() - start) * 1000

    threshold = config.performance.api_response_threshold_ms
    status = "PASS" if elapsed_ms <= threshold else "WARN"

    entry = {
        "label": label,
        "elapsed_ms": round(elapsed_ms, 2),
        "threshold_ms": threshold,
        "status": status,
    }
    _perf_log.append(entry)

    log_msg = f"[PERF] {label} → {elapsed_ms:.0f}ms (threshold {threshold}ms) [{status}]"
    if status == "WARN":
        logger.warning(log_msg)
    else:
        logger.info(log_msg)

    # Attach individual metric to Allure
    allure.attach(
        json.dumps(entry, indent=2),
        name=f"Perf: {label}",
        attachment_type=allure.attachment_type.JSON,
    )


def measure_page_load(driver: WebDriver, label: str = "Page Load") -> float:
    """
    Reads browser Navigation Timing API to calculate page load time in ms.

    Returns:
        Total page load duration in milliseconds.
    """
    nav_timing = driver.execute_script(
        """
        const t = window.performance.timing;
        return {
            navigationStart: t.navigationStart,
            loadEventEnd: t.loadEventEnd,
            domContentLoaded: t.domContentLoadedEventEnd - t.navigationStart,
            fullLoad: t.loadEventEnd - t.navigationStart
        };
        """
    )

    full_load_ms = nav_timing.get("fullLoad", 0)
    dom_ready_ms = nav_timing.get("domContentLoaded", 0)
    threshold = config.performance.page_load_threshold_ms
    status = "PASS" if full_load_ms <= threshold else "WARN"

    entry = {
        "label": label,
        "full_load_ms": full_load_ms,
        "dom_content_loaded_ms": dom_ready_ms,
        "threshold_ms": threshold,
        "status": status,
    }
    _perf_log.append(entry)

    log_msg = (
        f"[PERF] {label} → fullLoad={full_load_ms}ms | DOMReady={dom_ready_ms}ms "
        f"(threshold {threshold}ms) [{status}]"
    )
    if status == "WARN":
        logger.warning(log_msg)
    else:
        logger.info(log_msg)

    allure.attach(
        json.dumps(entry, indent=2),
        name=f"Perf: {label}",
        attachment_type=allure.attachment_type.JSON,
    )

    return float(full_load_ms)


def attach_perf_summary() -> None:
    """
    Attaches the full session performance log to Allure.
    Call this at the end of a test or in a fixture teardown.
    """
    if _perf_log:
        allure.attach(
            json.dumps(_perf_log, indent=2),
            name="Performance Summary",
            attachment_type=allure.attachment_type.JSON,
        )


def reset_perf_log() -> None:
    """Clears in-memory performance log (call between test runs if needed)."""
    global _perf_log
    _perf_log = []
