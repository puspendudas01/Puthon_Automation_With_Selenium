"""Assignment 2: Multiple Element Identification
Find several elements of the same type with find_elements() and work with the list."""
from selenium.webdriver.common.by import By
from common import start_browser, highlight, screenshot

driver = start_browser()
try:
    # All navigation links (same class)
    nav_links = driver.find_elements(By.CLASS_NAME, "nav-link")
    print(f"Navigation links found: {len(nav_links)}\n")
    for index, link in enumerate(nav_links, start=1):
        highlight(driver, link, pause=0.6)
        print(f"  {index}. {link.text}")
    assert len(nav_links) == 5

    # All <a> tags on the page (includes 'Forgot Password?')
    all_links = driver.find_elements(By.TAG_NAME, "a")
    print(f"\nTotal <a> tags on the page: {len(all_links)}")
    print("Their text:", [a.text for a in all_links])
    assert len(all_links) == 6

    # Work with the list: filter it in Python
    starting_with_c = [a.text for a in nav_links if a.text.startswith("C")]
    print("Navigation links starting with 'C':", starting_with_c)
    assert starting_with_c == ["Courses", "Contact"]

    screenshot(driver, "assignment2_multiple_elements")
    print("\nAssignment 2 PASSED")
finally:
    driver.quit()
