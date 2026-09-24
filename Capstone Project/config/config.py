"""Central configuration. Every value can be overridden with an environment variable."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_URL = os.getenv("BASE_URL", "https://automationexercise.com").rstrip("/")
BROWSER = os.getenv("BROWSER", "chrome").lower()          # chrome | firefox
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

SLOW_MO = float(os.getenv("SLOW_MO", "0"))
EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "15"))     # seconds
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "45"))

DATA_DIR = BASE_DIR / "data"
REPORT_DIR = BASE_DIR / "reports"
SCREENSHOT_DIR = REPORT_DIR / "screenshots"
JSON_DATA_FILE = DATA_DIR / "test_data.json"
EXCEL_DATA_FILE = DATA_DIR / "test_data.xlsx"

# Optional: use an existing account instead of registering a fresh one each run
EXISTING_EMAIL = os.getenv("TEST_EMAIL")
EXISTING_PASSWORD = os.getenv("TEST_PASSWORD")

for _d in (REPORT_DIR, SCREENSHOT_DIR):
    _d.mkdir(parents=True, exist_ok=True)
