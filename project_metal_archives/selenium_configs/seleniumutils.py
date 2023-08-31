from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium_configs.driversettings import DriverSettings


class SeleniumUtils(DriverSettings):
    def wait_element_enabled_id(self, element_id):
        return self.wait.until(EC.visibility_of_element_located((By.ID, element_id)))

    def wait_element_enabled_xpt(self, element_xpath):
        return self.wait.until(
            EC.visibility_of_element_located((By.XPATH, element_xpath))
        )

    def wait_elements_visible_xpt(self, element_xpath):
        return self.wait.until(
            EC.visibility_of_all_elements_located((By.XPATH, element_xpath))
        )

    def wait_element_enabled_tag(self, element_tagname):
        return self.wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, element_tagname))
        )

    def wait_element_enabled_name(self, element_name):
        return self.wait.until(
            EC.visibility_of_element_located((By.NAME, element_name))
        )

    def click_element_xpt(self, element_xpath):
        element = self.wait_element_enabled_xpt(element_xpath)
        element.click()

    def click_element_id(self, element_xpath):
        element = self.wait_element_enabled_id(element_xpath)
        element.click()

    def click_element_tag(self, element_xpath):
        element = self.wait_element_enabled_tag(element_xpath)
        element.click()

    def find_single_element(self, by: By, element):
        return self.driver.find_element(by, element)

    def find_multiple_elements(self, by: By, element):
        return self.driver.find_elements(by, element)

    def find_multiple_elements_xpath(self, element):
        return self.driver.find_elements(By.XPATH, element)

    def find_multiple_elements_tag(self, element):
        return self.driver.find_elements(By.TAG_NAME, element)

    def find_single_table_element(self, by: By, element):
        return self.driver.find_element(by, element)

    def find_multiple_table_elements(self, by: By, element):
        return self.driver.find_elements(by, element)

    def send_text_id(self, element_id, text):
        self.wait_element_enabled_id(element_id)
        field = self.find_single_element(By.ID, element_id)
        field.send_keys(text)

    def send_text_xpt(self, element_xpath, text):
        self.wait_element_enabled_xpt(element_xpath)
        field = self.find_single_element(By.XPATH, element_xpath)
        field.send_keys(text)

    def send_text_tag(self, element_tag_name, text):
        self.wait_element_enabled_tag(element_tag_name)
        field = self.find_single_element(By.TAG_NAME, element_tag_name)
        field.send_keys(text)

    def send_text_nme(self, element_name, text):
        self.wait_element_enabled_name(element_name)
        field = self.find_single_element(By.NAME, element_name)
        field.send_keys(text)

    def count_elements_xpt(self, element_xpath):
        ele_quantity = len(self.find_multiple_elements(By.XPATH, element_xpath))
        return ele_quantity

    def test_debug(self):
        print("Testing debug")
