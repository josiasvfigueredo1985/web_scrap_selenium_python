import importlib
import runpy
import sys
import unittest
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, call, patch


class MetalArchivesPageTest(unittest.TestCase):
    def setUp(self):
        selenium = ModuleType("selenium")
        webdriver = ModuleType("selenium.webdriver")
        webdriver.ChromeOptions = MagicMock()
        webdriver.Chrome = MagicMock()
        selenium.webdriver = webdriver
        by = ModuleType("selenium.webdriver.common.by")
        by.By = SimpleNamespace(ID="id", NAME="name", XPATH="xpath", TAG_NAME="tag name")
        ui = ModuleType("selenium.webdriver.support.ui")
        ui.WebDriverWait = MagicMock()
        openpyxl = ModuleType("openpyxl")
        openpyxl.Workbook = MagicMock()

        modules = {
            "selenium": selenium,
            "selenium.webdriver": webdriver,
            "selenium.webdriver.common": ModuleType("selenium.webdriver.common"),
            "selenium.webdriver.common.by": by,
            "selenium.webdriver.support": ModuleType("selenium.webdriver.support"),
            "selenium.webdriver.support.ui": ui,
            "selenium.webdriver.support.expected_conditions": ModuleType(
                "selenium.webdriver.support.expected_conditions"
            ),
            "openpyxl": openpyxl,
        }
        self.module_patch = patch.dict(sys.modules, modules)
        self.module_patch.start()
        self.addCleanup(self.module_patch.stop)
        for name in (
            "src.browser.driver_factory",
            "src.browser.driver_settings",
            "src.browser.selenium_utils",
            "src.pages.metal_archives_page",
            "src.scrapers.search_bands_by_location",
        ):
            sys.modules.pop(name, None)
        self.page_module = importlib.import_module(
            "src.pages.metal_archives_page"
        )
        self.page = self.page_module.MetalArchivesSearchPage()
        self.openpyxl = openpyxl

    def test_search_fields_use_the_expected_locators_and_settings(self):
        self.page.click_element_xpath = MagicMock()
        self.page.send_text_id = MagicMock()
        self.page.send_text_name = MagicMock()

        self.page.click_advanced_search_option()
        self.page.fill_genre_option()
        self.page.select_country_option()
        self.page.select_status_option()
        self.page.fill_location_option()
        self.page.click_perform_search_button()

        self.assertEqual(self.page.click_element_xpath.call_args_list, [
            call("//*[text()='Advanced search']"),
            call("(//*[@value='Perform search'])[1]"),
        ])
        self.assertEqual(self.page.send_text_id.call_args_list, [
            call("genre", self.page.genre_name),
            call("country", self.page.country_name),
            call("status", self.page.status_name),
        ])
        self.page.send_text_name.assert_called_once_with("location", self.page.location_name)

    def test_export_visits_each_page_and_writes_its_rows(self):
        self.page.wait_element_enabled_tag = MagicMock()
        self.page.count_elements_xpath = MagicMock(return_value=2)
        self.page.click_element_xpath = MagicMock()
        self.page.wait_elements_visible_xpath = MagicMock()
        rows = []
        for band in ("First", "Second"):
            row = MagicMock()
            row.find_elements.return_value = [
                SimpleNamespace(text=band),
                SimpleNamespace(text="Metal"),
                SimpleNamespace(text="Brazil"),
            ]
            rows.append([row])
        self.page.driver.find_elements.side_effect = rows
        workbook = self.openpyxl.Workbook.return_value

        self.page.save_data_from_search()

        self.page.count_elements_xpath.assert_called_once_with(
            "//*[@id='searchResultsBand_paginate']/span/a"
        )
        self.assertEqual(self.page.driver.find_elements.call_args_list, [
            call("xpath", "//*[@id='searchResultsBand']/tbody/tr"),
            call("xpath", "//*[@id='searchResultsBand']/tbody/tr"),
        ])
        for page_rows in rows:
            page_rows[0].find_elements.assert_called_once_with("tag name", "td")
        self.assertEqual(self.page.click_element_xpath.call_args_list, [
            call("//*[@id='searchResultsBand_paginate']/span/a[1]"),
            call("//*[@id='searchResultsBand_paginate']/span/a[2]"),
        ])
        self.assertEqual(workbook.active.append.call_args_list, [
            call(("Band", "Genre", "Location")),
            call(("First", "Metal", "Brazil")),
            call(("Second", "Metal", "Brazil")),
        ])
        workbook.save.assert_called_once_with("./Bandas_Brazil.xlsx")
        workbook.close.assert_called_once()

    def test_export_propagates_scraping_errors_and_closes_workbook(self):
        error = RuntimeError("search failed")
        self.page.wait_element_enabled_tag = MagicMock(side_effect=error)
        workbook = self.openpyxl.Workbook.return_value

        with self.assertRaisesRegex(RuntimeError, "search failed"):
            self.page.save_data_from_search()

        workbook.save.assert_not_called()
        workbook.close.assert_called_once_with()

    def test_export_propagates_save_errors_and_closes_workbook(self):
        self.page.wait_element_enabled_tag = MagicMock()
        self.page.count_elements_xpath = MagicMock(return_value=0)
        workbook = self.openpyxl.Workbook.return_value
        workbook.save.side_effect = PermissionError("cannot save workbook")

        with self.assertRaisesRegex(PermissionError, "cannot save workbook"):
            self.page.save_data_from_search()

        workbook.close.assert_called_once_with()

    def test_export_closes_workbook_when_header_append_fails(self):
        workbook = self.openpyxl.Workbook.return_value
        workbook.active.append.side_effect = ValueError("invalid header")

        with self.assertRaisesRegex(ValueError, "invalid header"):
            self.page.save_data_from_search()

        workbook.close.assert_called_once_with()

    def test_entry_point_runs_search_in_order(self):
        entry_point = importlib.import_module(
            "src.scrapers.search_bands_by_location"
        )
        with patch.object(entry_point, "MetalArchivesSearchPage") as page_class:
            entry_point.search_bands_for_brazil()

        self.assertEqual(page_class.return_value.method_calls, [
            call.click_advanced_search_option(),
            call.fill_genre_option(),
            call.select_country_option(),
            call.select_status_option(),
            call.fill_location_option(),
            call.click_perform_search_button(),
            call.save_data_from_search(),
            call.close_driver(),
        ])

    def test_entry_point_closes_driver_when_export_fails(self):
        entry_point = importlib.import_module("src.scrapers.search_bands_by_location")
        with patch.object(entry_point, "MetalArchivesSearchPage") as page_class:
            page_class.return_value.save_data_from_search.side_effect = PermissionError(
                "cannot save workbook"
            )
            with self.assertRaisesRegex(PermissionError, "cannot save workbook"):
                entry_point.search_bands_for_brazil()

        page_class.return_value.close_driver.assert_called_once_with()

    def test_module_entry_point_runs_the_search(self):
        with patch.object(self.page_module, "MetalArchivesSearchPage") as page_class:
            runpy.run_module(
                "src.scrapers.search_bands_by_location", run_name="__main__"
            )

        page_class.return_value.click_advanced_search_option.assert_called_once_with()
        page_class.return_value.close_driver.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
