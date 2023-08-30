from selenium_configs.driverfactory import DriverFactory
from selenium.webdriver.support.ui import WebDriverWait
from data.variables import Locators

base_url = Locators().base_url


class DriverSettings:
    "Centralization of the settings to be used by all modules"
    driver_factory = DriverFactory(browser="chrome", headless=False)
    driver = driver_factory.get_driver()
    driver.get(base_url)
    wait = WebDriverWait(driver, 10)
