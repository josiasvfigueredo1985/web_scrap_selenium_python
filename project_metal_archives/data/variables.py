class Locators:
    "Variables available to all modules that import this module"
    ##########  Variables  ##########
    base_url = "https://www.metal-archives.com/"

    ##########  Excel File  ##########
    filename = "./Bandas_"
    header = ("Band", "Genre", "Location")

    ##########  Advanced Search  ##########
    adv_search = "//*[text()='Advanced search']"
    genre = "(//*[@name='genre'])[1]"
    perf_search = "(//*[@value='Perform search'])[1]"
    bands_list = "//tbody[@role='alert']"
    genre_name = ""  # "Death Metal"
    genre_id = "genre"
    country_id = "country"
    country_name = "Brazil"
    status = [
        "(Any)",
        "Active",
        "On hold",
        "Split-up",
        "Unknown",
        "Changed name",
        "Disputed",
    ]
    status_id = "status"
    status_name = status[0]
    location_id = "location"
    location_name = "Minas Gerais"
    select_page_buttons = "//*[@id='searchResultsBand_paginate']/span/a"
    table_rows = "//*[@id='searchResultsBand']/tbody/tr"
