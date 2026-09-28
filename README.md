# Capstone Project: Automated Testing of an E-Commerce Web Application

**Selenium WebDriver + Python + Pytest (Page Object Model)**

**Author:** Puspendu Sekhar Das
**Application under test:** https://automationexercise.com  
**Demo video:** https://drive.google.com/file/d/1pkX96GqT6RkMuh8_j4sqUrbrSgKcwY-H/view?usp=sharing

---

## 1. Overview

This project automates the purchase journey of a customer on an e-commerce demo site. A single end-to-end test logs in, searches for a product, adds it to the cart, updates the quantity and verifies the cart details. Test data comes from Excel and JSON files, every step is captured as a screenshot, and an HTML execution report is generated on each run.

## 2. What the automation does

| # | Step | Where it is implemented |
|---|------|-------------------------|
| 1 | Launch browser | `utils/driver_factory.py` |
| 2 | Log in | `pages/auth_page.py` |
| 3 | Search product | `pages/product_page.py` |
| 4 | Add product to cart | `pages/product_page.py` |
| 5 | Update quantity | `pages/product_page.py` (product details page) |
| 6 | Verify cart details (name, quantity, price, total) | `pages/cart_page.py`, `tests/test_purchase_flow.py` |
| 7 | Capture screenshots | `utils/screenshot.py`, `tests/conftest.py` |
| 8 | Read test data from Excel / JSON | `utils/data_reader.py`, `data/` |
| 9 | Handle popups, alerts and ad overlays | `pages/base_page.py` |
| 10 | Generate execution report | `pytest.ini` (pytest-html) |

## 3. Folder contents

```
Folder 2 - Capstone Project/
├── README.md                    this file
├── report/                      project report (Capstone_Project_Report.docx / PDF)
├── source_code/
│   └── selenium_ecommerce_automation/
│       ├── main.py              entry point
│       ├── pytest.ini           report and logging settings
│       ├── requirements.txt
│       ├── config/              URL, browser, timeouts, paths
│       ├── data/                test_data.json, test_data.xlsx
│       ├── pages/               page objects (base, auth, product, cart)
│       ├── utils/               driver factory, data reader, screenshot helper
│       └── tests/               conftest.py, test_purchase_flow.py
├── outputs/                     execution_report.html, junit_results.xml, execution.log
├── screenshots/                 step screenshots captured during execution
└── demo_video_link.txt          link to the demonstration video
```

## 4. Prerequisites

- Python 3.10 or later
- Google Chrome (Firefox is also supported)
- Internet access (the tests run against the live demo site)

## 5. Setup and run

Open a terminal in `source_code/selenium_ecommerce_automation` and run:

```
pip install -r requirements.txt
python main.py
```

A virtual environment is optional but recommended:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Selenium Manager downloads the matching browser driver automatically, so no manual driver setup is needed.

### Options (environment variables)

| Variable | Purpose | Example (PowerShell) |
|----------|---------|----------------------|
| `HEADLESS` | Run without a visible browser | `$env:HEADLESS="true"` |
| `BROWSER` | `chrome` (default) or `firefox` | `$env:BROWSER="firefox"` |
| `BASE_URL` | Change the site under test | `$env:BASE_URL="https://automationexercise.com"` |
| `TEST_EMAIL`, `TEST_PASSWORD` | Use an existing account instead of registering a new one | `$env:TEST_EMAIL="you@mail.com"` |

Run a single product only: `python main.py -k "Blue Top"`

## 6. Test data

- `data/test_data.json`: user profile used for registration and login. A unique email is generated on every run.
- `data/test_data.xlsx` (sheet `Products`): one test runs per row.

| search_term | expected_name | extra_quantity |
|-------------|---------------|----------------|
| Blue Top | Blue Top | 2 |
| Men Tshirt | Men Tshirt | 3 |
| Sleeveless Dress | Sleeveless Dress | 1 |

To change the products, edit the Excel file or regenerate it with `python data/create_test_data.py`.

## 7. Outputs

Every run writes to the `reports/` folder inside the project:

| File | Description |
|------|-------------|
| `execution_report.html` | Self-contained HTML report with pass/fail status, logs and embedded screenshots |
| `junit_results.xml` | Machine-readable results (CI friendly) |
| `execution.log` | Step-by-step execution log |
| `screenshots/` | PNG screenshot for each step, plus one automatically on failure |

Open `execution_report.html` in any browser to view the results.

## 8. How the test verifies the cart

1. Adds the searched product from the results page and reads the cart quantity.
2. Opens the product details page, sets the extra quantity and adds it again (the site merges it into the same cart line).
3. Asserts there is one cart line, the name matches, quantity equals the earlier quantity plus the extra, the unit price matches the listing, and the line total equals price times quantity.
4. Clears the cart and logs out.

## 9. Troubleshooting

- **`No module named selenium`**: run `pip install -r requirements.txt` in the same Python you use to run `main.py`.
- **`python` not recognized (Windows)**: use `py main.py` and `py -m pip install -r requirements.txt`.
- **Ads or popups blocking clicks**: handled automatically; if a run still fails, check the failure screenshot in `execution_report.html`.
- **Account cleanup warning at the end of a run**: the throw-away test account could not be deleted because the page was slow. It does not affect test results.
- **Slow network**: increase the wait, e.g. `$env:EXPLICIT_WAIT="30"`.

## 10. Notes

- The application is a public demo site. Its pages, ads or speed can change and may occasionally affect a run.
- Checkout and payment are outside the scope of this project.
