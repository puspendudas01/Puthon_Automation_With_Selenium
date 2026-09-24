"""Shopping cart page."""
import logging
import re
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

log = logging.getLogger(__name__)


def money(text: str) -> int:
    """'Rs. 1,500' -> 1500"""
    return int(re.sub(r"[^\d]", "", text) or 0)


class CartPage(BasePage):
    ROWS = (By.CSS_SELECTOR, "#cart_info_table tbody tr")
    DELETE = (By.CSS_SELECTOR, "a.cart_quantity_delete")

    def open_cart(self):
        self.open("/view_cart")

    def get_items(self) -> list[dict]:
        items = []
        for row in self.driver.find_elements(*self.ROWS):
            items.append({
                "name": row.find_element(By.CSS_SELECTOR, ".cart_description h4 a").text.strip(),
                "price": money(row.find_element(By.CSS_SELECTOR, ".cart_price p").text),
                "quantity": int(row.find_element(By.CSS_SELECTOR, ".cart_quantity button").text.strip()),
                "total": money(row.find_element(By.CSS_SELECTOR, ".cart_total_price").text),
            })
        log.info("Cart contents: %s", items)
        return items

    def clear_cart(self):
        self.open_cart()
        while True:
            buttons = self.driver.find_elements(*self.DELETE)
            if not buttons:
                break
            before = len(buttons)
            self.click(self.DELETE)
            self.wait.until(lambda d: len(d.find_elements(*self.DELETE)) < before)
        log.info("Cart cleared")
