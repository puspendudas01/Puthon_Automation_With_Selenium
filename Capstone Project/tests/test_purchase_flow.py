"""End-to-end purchase flow, data-driven from Excel (products) and JSON (user)."""
import logging
import pytest

from config import config
from pages.auth_page import AuthPage
from pages.cart_page import CartPage
from pages.product_page import ProductPage
from utils.data_reader import read_excel

log = logging.getLogger(__name__)

PRODUCTS = read_excel(config.EXCEL_DATA_FILE, "Products")

def norm(text: str) -> str:
    return " ".join(text.split()).lower()


@pytest.mark.e2e
@pytest.mark.parametrize("product", PRODUCTS, ids=[p["search_term"] for p in PRODUCTS])
def test_purchase_flow(driver, snap, registered_user, product):
    term = product["search_term"]
    expected_name = product["expected_name"]
    extra_qty = int(product["extra_quantity"])

    auth, products, cart = AuthPage(driver), ProductPage(driver), CartPage(driver)

    # 1. Launch browser / open application
    auth.open("/")
    assert "Automation Exercise" in driver.title
    snap("01_home_page")

    # 2. Login
    auth.login(registered_user["email"], registered_user["password"])
    assert auth.is_logged_in(), "Login failed - 'Logged in as' banner not shown"
    snap("02_logged_in")
    cart.clear_cart()                      # start every scenario with an empty cart

    # 3. Search product
    count = products.search(term)
    assert count > 0, f"No results for '{term}'"
    name = products.first_result_name()
    unit_price = products.first_result_price()
    assert norm(expected_name) in norm(name)
    snap("03_search_results")

    # 4. Add product to cart (+ popup handling inside the page object)
    products.add_first_result_to_cart()
    snap("04_added_to_cart_modal")
    products.go_to_cart_from_modal()
    items = cart.get_items()
    assert len(items) == 1
    initial_qty = items[0]["quantity"]
    snap("05_cart_after_first_add")

    # 5. Update quantity (product page -> set quantity -> add again; site merges the line)
    products.search(term)
    products.open_first_result_details()
    products.add_from_detail_page(extra_qty)
    snap("06_quantity_updated_modal")
    products.go_to_cart_from_modal()

    # 6. Verify cart details
    items = cart.get_items()
    assert len(items) == 1, "Same product should stay a single cart line"
    item = items[0]
    assert norm(expected_name) in norm(item["name"])
    assert item["quantity"] == initial_qty + extra_qty
    assert item["price"] == int("".join(ch for ch in unit_price if ch.isdigit()))
    assert item["total"] == item["price"] * item["quantity"]

    # 7. Screenshot of the verified cart
    snap("07_cart_verified")
    log.info("PASS: %s x%s = Rs. %s", item["name"], item["quantity"], item["total"])

    # cleanup
    cart.clear_cart()
    auth.logout()
