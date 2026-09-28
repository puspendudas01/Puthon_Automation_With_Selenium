"""Assignment 3: CSS Selector Challenge
Locate elements with CSS wildcard (attribute) selectors for dynamic attribute values."""
from selenium.webdriver.common.by import By
from common import start_browser, highlight, screenshot

driver = start_browser()
try:
    def show(title, selector, expected):
        found = driver.find_elements(By.CSS_SELECTOR, selector)
        print(f"{title}\n  selector: {selector}\n  found: {len(found)}")
        for el in found:
            highlight(driver, el, pause=0.6)
            print(f"    id={el.get_attribute('id')!r:22} text={el.text!r}")
        assert len(found) == expected, f"expected {expected}, got {len(found)}"
        print()

    # ^=  id STARTS WITH 'user_'   (the example given in the assignment)
    show("1. ID starts with 'user_'", "[id^='user_']", 3)

    # *=  id CONTAINS 'user'  (scoped to the members section, because the
    #     login field id="username" also contains the text 'user')
    show("2. ID contains 'user' (inside #assignment3)", "#assignment3 [id*='user']", 4)

    # $=  id ENDS WITH '_admin'
    show("3. ID ends with '_admin'", "[id$='_admin']", 1)

    screenshot(driver, "assignment3_css_wildcards")
    print("Assignment 3 PASSED")
finally:
    driver.quit()
