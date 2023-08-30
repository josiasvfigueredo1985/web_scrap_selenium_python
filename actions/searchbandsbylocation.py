from steps.metalarchivespage import MetalArchivesSearchPage


def search_bands_for_brazil():
    metal = MetalArchivesSearchPage()

    metal.click_advanced_search_option()
    metal.fill_genre_option()
    metal.select_country_option()
    metal.select_status_option()
    metal.fill_location_option()
    metal.click_perform_search_button()
    metal.save_data_from_search()
    metal.close_driver()


if __name__ == "__main__":
    search_bands_for_brazil()
