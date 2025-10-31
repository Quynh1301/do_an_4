import pytest
from selenium import webdriver
import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
import pytest

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            screenshot_path = f"artifacts/screenshots/{item.name}.png"
            driver.save_screenshot(screenshot_path)
            if hasattr(report, "extra"):
                pytest_html = item.config.pluginmanager.getplugin("html")
                extra = getattr(report, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                report.extra = extra
