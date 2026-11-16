from typing import ClassVar


class SearchSettings:
    "Settings for the Metal Archives search and Excel export."
    base_url = "https://www.metal-archives.com/"

    filename = "./Bandas_"
    header = ("Band", "Genre", "Location")

    genre_name = ""  # "Death Metal"
    country_name = "Brazil"
    status: ClassVar[list[str]] = [
        "(Any)",
        "Active",
        "On hold",
        "Split-up",
        "Unknown",
        "Changed name",
        "Disputed",
    ]
    status_name = status[0]
    location_name = "Minas Gerais"
