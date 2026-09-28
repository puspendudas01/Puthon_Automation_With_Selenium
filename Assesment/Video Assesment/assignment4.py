"""Assignment 4: Child Nodes Using CSS
Locate a button inside a specific div using the CSS child combinator (>) and click it."""
from selenium.webdriver.common.by import By
from common import start_browser, highlight, screenshot

driver = start_browser()
try:
    # Direct child <button> of the div with id 'profile-card'
    button = driver.find_element(By.CSS_SELECTOR, "#profile-card > button")
    highlight(driver, button)
    print(f"Button located inside #profile-card: '{button.text}'")

    # Other direct children of the same div
    name = driver.find_element(By.CSS_SELECTOR, "#profile-card > h3").text
    role = driver.find_element(By.CSS_SELECTOR, "#profile-card > p").text
    print(f"Card owner: {name} | {role}")

    # Interact with it
    button.click()
    status = driver.find_element(By.CSS_SELECTOR, "#status")
    highlight(driver, status)
    assert status.text == "Profile opened successfully"
    print(f"After click, status message: '{status.text}'")

    screenshot(driver, "assignment4_child_selector")
    print("\nAssignment 4 PASSED")
finally:
    driver.quit()
