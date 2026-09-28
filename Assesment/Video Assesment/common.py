"""Shared helpers for the four Selenium assignments."""
import time
from pathlib import Path
from selenium import webdriver

BASE = Path(__file__).resolve().parent
PAGE_URL = (BASE / "demo_page.html").as_uri()
SHOTS = BASE / "screenshots"
SHOTS.mkdir(exist_ok=True)

PAUSE = 1.5   # seconds between steps so the screen recording is easy to follow


def start_browser():
    """Opens Chrome (Selenium Manager downloads the driver automatically) and loads the demo page."""
    opts = webdriver.ChromeOptions()
    opts.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=opts)
    driver.get(PAGE_URL)
    time.sleep(PAUSE)
    return driver


def highlight(driver, element, pause=PAUSE):
    """Scrolls to the element and outlines it in red so the viewer can see what was located."""
    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});"
        "arguments[0].style.outline='3px solid red';", element)
    time.sleep(pause)


def screenshot(driver, name):
    path = SHOTS / f"{name}.png"
    driver.save_screenshot(str(path))
    print(f"Screenshot saved: screenshots/{path.name}")
