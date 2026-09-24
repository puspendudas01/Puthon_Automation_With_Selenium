"""Creates a configured WebDriver (Selenium Manager downloads the driver automatically)."""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from config import config


def create_driver():
    if config.BROWSER == "firefox":
        opts = FirefoxOptions()
        opts.page_load_strategy = "eager"
        if config.HEADLESS:
            opts.add_argument("-headless")
        driver = webdriver.Firefox(options=opts)
        driver.maximize_window()
    else:
        opts = ChromeOptions()
        opts.page_load_strategy = "eager"          # don't wait for ad/tracker resources
        opts.add_argument("--disable-notifications")
        opts.add_argument("--disable-infobars")
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        if config.HEADLESS:
            opts.add_argument("--headless=new")
            opts.add_argument("--window-size=1920,1080")
        else:
            opts.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=opts)

    driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    return driver
