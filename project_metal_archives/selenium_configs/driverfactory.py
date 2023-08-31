from selenium import webdriver
from data.browsers import Browsers


class DriverFactory:
    'Return driver for the given browser and driver options.'

    def __init__(self, browser, headless: bool):
        'Constructor for Driver Factory.'
        self.browser = browser
        self.headless = headless

    def get_driver(self):
        'Return driver according to the given parameters.'
        if self.browser.lower() == Browsers.Chrome.value:
            options = webdriver.ChromeOptions()
            if (self.headless):
                options.add_argument('--headless')
            return webdriver.Chrome(options=options)
        elif self.browser.lower() == Browsers.Firefox.value:
            options = webdriver.FirefoxOptions()
            if (self.headless):
                options.add_argument('--headless')
            return webdriver.Firefox()
        elif self.browser.lower() == Browsers.Edge.value:
            options = webdriver.EdgeOptions()
            if (self.headless):
                options.add_argument('--headless')
            return webdriver.Edge()
        elif self.browser.lower() == Browsers.Safari.value:
            if (self.headless):
                raise ValueError(
                    'Headless mode not available for Safari browser')
            return webdriver.Safari()
        else:
            raise ValueError("Unsupported browser")
