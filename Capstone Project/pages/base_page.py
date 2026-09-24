"""Base Page Object: waits, safe clicks, alert + overlay handling."""
import logging
import time
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from config import config

log = logging.getLogger(__name__)

_REMOVE_ADS_JS = """
document.querySelectorAll(
  'ins.adsbygoogle, .adsbygoogle, iframe[id^="aswift"], iframe[id^="google_ads"],'
  + '[id^="google_ads_iframe"], #ad_position_box, .google-auto-placed'
).forEach(e => e.remove());
"""


class BasePage:
    CONSENT_BUTTON = (By.CSS_SELECTOR, ".fc-consent-root .fc-cta-consent")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, config.EXPLICIT_WAIT)

    def _pause(self, factor: float = 1.0):
        if config.SLOW_MO > 0:
            time.sleep(config.SLOW_MO * factor)

    def _highlight(self, element):
        if config.SLOW_MO > 0:
            try:
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block:'center'});"
                    "arguments[0].style.outline='3px solid red';"
                    "arguments[0].style.outlineOffset='2px';", element)
            except Exception:
                pass

    # ---------- navigation ----------
    def open(self, path: str = "/"):
        url = f"{config.BASE_URL}{path}"
        log.info("Opening %s", url)
        self.driver.get(url)
        self.dismiss_overlays()
        self._pause(1.5)

    # ---------- element helpers ----------
    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        try:
            el = self.wait.until(EC.element_to_be_clickable(locator))
            self._highlight(el)
            self._pause()
            el.click()
        except (ElementClickInterceptedException, TimeoutException):
            log.warning("Click on %s intercepted - removing overlays, using JS click", locator)
            self.remove_ads()
            el = self.find(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            self.driver.execute_script("arguments[0].click();", el)
        self._pause()

    def type(self, locator, text: str):
        el = self.visible(locator)
        self._highlight(el)
        self._pause(0.5)
        el.clear()
        if config.SLOW_MO > 0:
            for ch in text:
                el.send_keys(ch)
                time.sleep(0.08)
        else:
            el.send_keys(text)
        self._pause()

    def select_by_text(self, locator, text: str):
        el = self.visible(locator)
        self._highlight(el)
        self._pause(0.5)
        Select(el).select_by_visible_text(text)
        self._pause()

    def text_of(self, locator) -> str:
        return self.visible(locator).text.strip()

    def is_present(self, locator, timeout: int = 3) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # ---------- popups / alerts / overlays ----------
    def accept_alert_if_present(self, timeout: int = 2):
        """Handles a JS alert/confirm if one appears. Returns its text, or None."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            text = alert.text
            log.info("JS alert detected: %r - accepting", text)
            alert.accept()
            return text
        except TimeoutException:
            return None

    def remove_ads(self):
        try:
            self.driver.execute_script(_REMOVE_ADS_JS)
        except Exception:  # noqa: BLE001 - ad cleanup must never fail a test
            pass

    def dismiss_overlays(self):
        """Cookie/consent dialog + ad overlays (Google vignette) commonly shown on the demo site."""
        try:
            btns = self.driver.find_elements(*self.CONSENT_BUTTON)
            if btns and btns[0].is_displayed():
                log.info("Consent dialog detected - accepting")
                btns[0].click()
        except Exception:  # noqa: BLE001
            pass
        self.remove_ads()
        if "google_vignette" in self.driver.current_url:
            self.driver.execute_script("history.replaceState(null, '', location.pathname);")
