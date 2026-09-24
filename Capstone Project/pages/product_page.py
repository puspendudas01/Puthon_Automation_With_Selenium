"""Product search, listing and product-detail pages."""
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

log = logging.getLogger(__name__)


class ProductPage(BasePage):
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BTN = (By.ID, "submit_search")
    RESULTS_TITLE = (By.CSS_SELECTOR, ".features_items h2.title")
    RESULT_CARDS = (By.CSS_SELECTOR, ".features_items .product-image-wrapper")
    FIRST_NAME = (By.CSS_SELECTOR, ".features_items .productinfo p")
    FIRST_PRICE = (By.CSS_SELECTOR, ".features_items .productinfo h2")
    FIRST_ADD_BTN = (By.CSS_SELECTOR, ".features_items .productinfo a.add-to-cart")
    FIRST_VIEW_LINK = (By.CSS_SELECTOR, ".features_items .choose a[href^='/product_details']")
    # detail page
    DETAIL_NAME = (By.CSS_SELECTOR, ".product-information h2")
    QUANTITY = (By.ID, "quantity")
    DETAIL_ADD_BTN = (By.CSS_SELECTOR, "button.cart")
    # add-to-cart modal
    MODAL = (By.ID, "cartModal")
    MODAL_VIEW_CART = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    def search(self, term: str) -> int:
        log.info("Searching for %r", term)
        self.open("/products")
        self.type(self.SEARCH_INPUT, term)
        self.click(self.SEARCH_BTN)
        self.wait.until(lambda d: "searched products" in d.find_element(*self.RESULTS_TITLE).text.lower())        
        return len(self.driver.find_elements(*self.RESULT_CARDS))

    def first_result_name(self) -> str:
        return self.text_of(self.FIRST_NAME)

    def first_result_price(self) -> str:
        return self.text_of(self.FIRST_PRICE)

    def add_first_result_to_cart(self):
        log.info("Adding first search result to cart")
        self.click(self.FIRST_ADD_BTN)
        self.visible(self.MODAL)
        self.accept_alert_if_present(timeout=1)

    def open_first_result_details(self):
        self.click(self.FIRST_VIEW_LINK)
        self.visible(self.DETAIL_NAME)

    def add_from_detail_page(self, quantity: int):
        log.info("Setting quantity to %s on product detail page and adding to cart", quantity)
        self.type(self.QUANTITY, str(quantity))
        self.click(self.DETAIL_ADD_BTN)
        self.visible(self.MODAL)
        self.accept_alert_if_present(timeout=1)

    def go_to_cart_from_modal(self):
        self.click(self.MODAL_VIEW_CART)
