from selenium.webdriver.common.by import By
from src.browser.selenium_utils import SeleniumUtils
from src.config.search_settings import SearchSettings
import openpyxl


class MetalArchivesSearchPage(SeleniumUtils, SearchSettings):
    ADVANCED_SEARCH = "//*[text()='Advanced search']"
    GENRE = "genre"
    COUNTRY = "country"
    STATUS = "status"
    LOCATION = "location"
    PERFORM_SEARCH = "(//*[@value='Perform search'])[1]"
    PAGE_BUTTONS = "//*[@id='searchResultsBand_paginate']/span/a"
    PAGE_BUTTON = "//*[@id='searchResultsBand_paginate']/span/a[{}]"
    TABLE_ROWS = "//*[@id='searchResultsBand']/tbody/tr"
    TABLE_CELL = "td"

    def test_debug_page(self):
        self.test_debug()

    def click_advanced_search_option(self):
        self.click_element_xpath(self.ADVANCED_SEARCH)

    def fill_genre_option(self):
        "Fill Genre option field"
        self.send_text_id(self.GENRE, self.genre_name)

    def select_country_option(self):
        "Select Country option dropdown list"
        self.send_text_id(self.COUNTRY, self.country_name)

    def select_status_option(self):
        "Select Status option dropdown list"
        self.send_text_id(self.STATUS, self.status_name)

    def fill_location_option(self):
        "Fill City/state/province option field"
        self.send_text_name(self.LOCATION, self.location_name)

    def click_perform_search_button(self):
        "Click Perform Search button"
        self.click_element_xpath(self.PERFORM_SEARCH)

    def save_data_from_search(self):
        "Save data from search results to Excel file"
        workbook = openpyxl.Workbook()
        try:
            sheet = workbook.active
            sheet.append(self.header)
            self.wait_element_enabled_tag(self.TABLE_CELL)
            page_count = self.count_elements_xpath(self.PAGE_BUTTONS)
            for page_index in range(page_count):
                self.click_element_xpath(self.PAGE_BUTTON.format(page_index + 1))
                self.wait_elements_visible_xpath(self.TABLE_ROWS)
                rows = self.driver.find_elements(By.XPATH, self.TABLE_ROWS)
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, self.TABLE_CELL)
                    self.wait_element_enabled_tag(self.TABLE_CELL)
                    band_name = cells[0].text
                    genre = cells[1].text
                    location = cells[2].text
                    data = (band_name, genre, location)
                    sheet.append(data)
            print("Data successfully fetched, creating Excel sheet...")
            full_filename = self.filename + self.country_name + ".xlsx"
            workbook.save(full_filename)
            print("File successfully created with the name:\n" + full_filename)
            print("The file creation was finished.")
        finally:
            workbook.close()

    def close_driver(self):
        self.driver.quit()
