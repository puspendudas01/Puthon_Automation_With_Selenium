"""Fixtures + pytest-html integration (screenshots embedded in the report)."""
import logging
import os
import time

import pytest
from pytest_html import extras

from config import config as app_config
from pages.auth_page import AuthPage
from utils.data_reader import read_json
from utils.driver_factory import create_driver
from utils.screenshot import take_screenshot, to_base64

log = logging.getLogger(__name__)


# ---------------------------------------------------------------- report hooks
def pytest_configure(config):
    try:
        from pytest_metadata.plugin import metadata_key
        meta = config.stash[metadata_key]
        meta["Application"] = app_config.BASE_URL
        meta["Browser"] = app_config.BROWSER + (" (headless)" if app_config.HEADLESS else "")
    except Exception:  # noqa: BLE001
        pass


def pytest_html_report_title(report):
    report.title = "Selenium E-Commerce Purchase Flow - Execution Report"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return
    shots = list(getattr(item, "screenshots", []))
    driver = item.funcargs.get("driver")
    if report.failed and driver is not None:
        try:
            shots.append(take_screenshot(driver, f"FAILED_{item.name}"))
        except Exception:  # noqa: BLE001
            pass
    report_extras = getattr(report, "extras", [])
    for path in shots:
        report_extras.append(extras.png(to_base64(path), name=os.path.basename(str(path))))
    report.extras = report_extras


# ---------------------------------------------------------------- fixtures
@pytest.fixture(scope="session")
def test_data():
    return read_json(app_config.JSON_DATA_FILE)


@pytest.fixture(scope="session")
def registered_user(test_data):
    """Provides credentials. Registers a throw-away account unless TEST_EMAIL/TEST_PASSWORD are set."""
    if app_config.EXISTING_EMAIL and app_config.EXISTING_PASSWORD:
        yield {"email": app_config.EXISTING_EMAIL, "password": app_config.EXISTING_PASSWORD}
        return

    email = f"{test_data['email_prefix']}.{int(time.time())}@{test_data['email_domain']}"
    user = test_data["user"]
    creds = {"email": email, "password": user["password"]}

    driver = create_driver()
    try:
        auth = AuthPage(driver)
        auth.register(user, email)
        auth.logout()
    finally:
        driver.quit()
    log.info("Test account created: %s", email)

    yield creds

    driver = create_driver()          # teardown: remove the throw-away account
    try:
        auth = AuthPage(driver)
        auth.login(creds["email"], creds["password"])
        auth.delete_account()
        log.info("Test account deleted")
    except Exception as exc:  # noqa: BLE001
        log.warning("Account cleanup failed: %s", exc)
    finally:
        driver.quit()


@pytest.fixture
def driver(request):
    drv = create_driver()
    request.node.screenshots = []
    yield drv
    drv.quit()


@pytest.fixture
def snap(driver, request):
    """snap('step_name') -> saves a screenshot and attaches it to the HTML report."""
    def _snap(name: str):
        if app_config.SLOW_MO > 0:
            time.sleep(app_config.SLOW_MO * 2)
        path = take_screenshot(driver, f"{request.node.name}_{name}")
        request.node.screenshots.append(path)
        log.info("Screenshot saved: %s", path.name)
        return path
    return _snap
