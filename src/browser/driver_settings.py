from src.browser.driver_factory import DriverFactory
from selenium.webdriver.support.ui import WebDriverWait
from src.config.search_settings import SearchSettings

base_url = SearchSettings().base_url


class DriverSettings:
    "Centralization of the settings to be used by all modules"
    driver_factory = DriverFactory(browser="chrome", headless=True)
    driver = driver_factory.get_driver()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
