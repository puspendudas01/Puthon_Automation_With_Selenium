"""Assignment 1: Web Element Identification
Locate web elements using By.ID, By.NAME, By.TAG_NAME, By.LINK_TEXT and By.CLASS_NAME."""
from selenium.webdriver.common.by import By
from common import start_browser, highlight, screenshot

driver = start_browser()
try:
    # 1. By.ID - username field
    username = driver.find_element(By.ID, "username")
    highlight(driver, username)
    username.send_keys("puspendu_qa")
    print("By.ID         -> username field located and text entered")

    # 2. By.NAME - password field
    password = driver.find_element(By.NAME, "password")
    highlight(driver, password)
    password.send_keys("Test@12345")
    print("By.NAME       -> password field located and text entered")

    # 3. By.TAG_NAME - page heading
    heading = driver.find_element(By.TAG_NAME, "h1")
    highlight(driver, heading)
    assert heading.text == "QA Practice Portal"
    print(f"By.TAG_NAME   -> heading located: '{heading.text}'")

    # 4. By.LINK_TEXT - forgot password link
    link = driver.find_element(By.LINK_TEXT, "Forgot Password?")
    highlight(driver, link)
    assert link.is_displayed()
    print(f"By.LINK_TEXT  -> link located: '{link.text}'")

    # 5. By.CLASS_NAME - login button
    button = driver.find_element(By.CLASS_NAME, "login-btn")
    highlight(driver, button)
    assert button.text == "Login"
    print(f"By.CLASS_NAME -> button located: '{button.text}'")

    screenshot(driver, "assignment1_locators")
    print("\nAssignment 1 PASSED: all 5 locator strategies worked")
finally:
    driver.quit()
