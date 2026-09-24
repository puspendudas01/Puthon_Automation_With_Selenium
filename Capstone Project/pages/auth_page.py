"""Signup / Login / Logout."""
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class AuthPage(BasePage):
    # login
    LOGIN_EMAIL = (By.CSS_SELECTOR, "input[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "input[data-qa='login-password']")
    LOGIN_BTN = (By.CSS_SELECTOR, "button[data-qa='login-button']")
    LOGGED_IN_AS = (By.XPATH, "//a[contains(.,'Logged in as')]")
    LOGOUT = (By.CSS_SELECTOR, "a[href='/logout']")
    # signup
    SIGNUP_NAME = (By.CSS_SELECTOR, "input[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "input[data-qa='signup-email']")
    SIGNUP_BTN = (By.CSS_SELECTOR, "button[data-qa='signup-button']")
    ACCOUNT_CREATED = (By.CSS_SELECTOR, "h2[data-qa='account-created']")
    CONTINUE = (By.CSS_SELECTOR, "a[data-qa='continue-button']")
    ACCOUNT_DELETED = (By.CSS_SELECTOR, "h2[data-qa='account-deleted']")

    def register(self, user: dict, email: str):
        log.info("Registering new account %s", email)
        self.open("/login")
        self.type(self.SIGNUP_NAME, user["name"])
        self.type(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BTN)

        radio = "#id_gender1" if user["title"].lower() == "mr" else "#id_gender2"
        self.click((By.CSS_SELECTOR, radio))
        self.type((By.ID, "password"), user["password"])
        self.select_by_text((By.ID, "days"), user["birth_day"])
        self.select_by_text((By.ID, "months"), user["birth_month"])
        self.select_by_text((By.ID, "years"), user["birth_year"])
        for field, key in (("first_name", "first_name"), ("last_name", "last_name"),
                           ("company", "company"), ("address1", "address"),
                           ("address2", "address2"), ("state", "state"),
                           ("city", "city"), ("zipcode", "zipcode"),
                           ("mobile_number", "mobile")):
            self.type((By.ID, field), user[key])
        self.select_by_text((By.ID, "country"), user["country"])
        self.click((By.CSS_SELECTOR, "button[data-qa='create-account']"))
        self.visible(self.ACCOUNT_CREATED)
        self.click(self.CONTINUE)

    def login(self, email: str, password: str):
        log.info("Logging in as %s", email)
        self.open("/login")
        self.type(self.LOGIN_EMAIL, email)
        self.type(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BTN)
        self.accept_alert_if_present(timeout=1)

    def is_logged_in(self) -> bool:
        return self.is_present(self.LOGGED_IN_AS, timeout=8)

    def logout(self):
        self.click(self.LOGOUT)

    def delete_account(self):
        self.open("/delete_account")
        self.visible(self.ACCOUNT_DELETED)
