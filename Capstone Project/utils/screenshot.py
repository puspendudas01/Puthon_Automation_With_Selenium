"""Screenshot + report helpers."""
import base64
import re
from datetime import datetime
from pathlib import Path
from config import config


def take_screenshot(driver, name: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    path = config.SCREENSHOT_DIR / f"{stamp}_{safe}.png"
    driver.save_screenshot(str(path))
    return path


def to_base64(path) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")
