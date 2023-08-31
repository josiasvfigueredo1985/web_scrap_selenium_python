from selenium_configs.driversettings import DriverSettings
from selenium.webdriver.common.by import By
from selenium_configs.seleniumutils import SeleniumUtils
from data.variables import Locators
import openpyxl
import os


class MetalArchivesSearchPage(SeleniumUtils, DriverSettings, Locators):
    def test_debug_page(self):
        self.test_debug()

    def click_advanced_search_option(self):
        self.click_element_xpt(self.adv_search)

    def fill_genre_option(self):
        "Fill Genre option field"
        self.send_text_id(self.genre_id, self.genre_name)

    def select_country_option(self):
        "Select Country option dropdown list"
        self.send_text_id(self.country_id, self.country_name)

    def select_status_option(self):
        "Select Status option dropdown list"
        self.send_text_id(self.status_id, self.status_name)

    def fill_location_option(self):
        "Fill City/state/province option field"
        self.send_text_nme(self.location_id, self.location_name)

    def click_perform_search_button(self):
        "Click Perform Search button"
        self.click_element_xpt(self.perf_search)

    def save_data_from_search(self):
        "Save data from search results to Excel file"
        ##########  Crete Excel SpreadSheet #########
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(self.header)
        #############################################
        try:
            self.wait_element_enabled_tag("td")
            buttons_qty = self.count_elements_xpt(self.select_page_buttons)
            for i in range(buttons_qty):
                self.click_element_xpt(
                    f"//*[@id='searchResultsBand_paginate']/span/a[{i+1}]"
                )
                self.wait_elements_visible_xpt(self.table_rows)
                # Variable to store the table information by each row found in table rows
                # This allows to use only 2 for loops, to fetch data hierarchically the following structure must be followed
                # table body-> tbody
                #   table rows->  tr
                #       table data-> td
                # In order to fetch data from each row and column, is necessary to use one  loop for each
                # table structure
                # The following variable is fetching data from each row and column with XPATH method
                # This way we can easily fetch data directly from table data and fetch each data by index
                table = self.driver.find_elements(By.XPATH, self.table_rows)
                for tbr in table:
                    tbc = tbr.find_elements(By.TAG_NAME, "td")
                    self.wait_element_enabled_tag("td")
                    # Fetch data from the array variable by positions
                    band_name = tbc[0].text
                    genre = tbc[1].text
                    location = tbc[2].text
                    # Tuple to store data for append each line in the Excel file
                    data = (band_name, genre, location)
                    sheet.append(data)
            print("Data successfully fetched, creating Excel sheet...")
            try:
                full_filename = self.filename + self.country_name + ".xlsx"
                workbook.save(full_filename)
                print("File successfully created with the name:\n" + full_filename)
            except Exception:
                print("Something went wrong to create the Excel sheet")
            finally:
                print("The file creation was finished.")
        except Exception:
            print("Something went wrong... :-(")
        finally:
            workbook.close()

    def close_driver(self):
        self.driver.quit()
