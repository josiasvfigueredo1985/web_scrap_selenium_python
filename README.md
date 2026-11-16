# Web Scraping with Python and Selenium

This learning project searches [Metal Archives](https://www.metal-archives.com/)
for bands and exports the results to an Excel workbook. The current script uses
the search criteria in `src/config/search_settings.py`.

## Requirements and setup

- Python 3 and its `pip` module.
- For the scraper: Google Chrome, internet access, and the Python packages
  [Selenium](https://www.selenium.dev/documentation/webdriver/) and
  [openpyxl](https://openpyxl.readthedocs.io/).
- For VS Code testing: [VS Code](https://code.visualstudio.com/) and the
  [Python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python).

From the repository root, create a virtual environment and install the scraper
dependencies. These commands use PowerShell on Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install selenium openpyxl
```

Selenium drives Chrome in headless mode. Selenium Manager can obtain a matching
driver when needed; that and accessing Metal Archives require network access.
The unit tests below use mocks and do not require Chrome, network access, Selenium
or openpyxl to be installed.

## Running the scraper

From the repository root, using the virtual environment created above:

```powershell
.\.venv\Scripts\python.exe -m src.scrapers.search_bands_by_location
```

By default, the search uses Brazil, Minas Gerais, any status, and an empty genre.
Edit `src/config/search_settings.py` to change the criteria or output filename.
The workbook is saved as `Bandas_Brazil.xlsx` in the current working directory
and an existing file with that name may be overwritten. Scraping and export
errors are reported to the caller; the browser and workbook are closed on failure.

## Running the tests

The tests use Python's built-in `unittest` and mock the Selenium browser and
openpyxl workbook. They check the search flow, selectors, export handling, and
error cleanup; they do not verify the live website or create a real workbook.

### Command line

Open a terminal in the repository root and run all tests:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Alternatively, replace `python` with `.\.venv\Scripts\python.exe` to use the
virtual environment. To run a single test:

```powershell
python -m unittest tests.test_metal_archives_page.MetalArchivesPageTest.test_export_visits_each_page_and_writes_its_rows -v
```

### VS Code

1. Open the repository root as the VS Code folder and install the Python extension.
2. Run **Python: Select Interpreter** from the Command Palette and select the
   Python interpreter you want to use, such as `.venv`.
3. Open **Testing** in the Activity Bar and select **Refresh Tests**. The workspace
   settings already enable `unittest` discovery under `tests/` for `test_*.py`.
4. Select **Run Tests** to run the suite, or use the run or debug icon next to an
   individual test. Inspect failures and output in the Testing view.

If no tests appear, confirm the repository root is open, a Python interpreter is
selected, and refresh test discovery.

### GitHub Actions report

The workflow runs the mocked tests on pull requests, pushes to `main`, and
manual runs. Each run uploads a downloadable HTML report when one is generated.
Runs on `main` also publish the latest report to GitHub Pages, including when
tests fail. The deployment job prints the browser link and adds it to the run
summary; pull request reports must be downloaded from the run's artifacts.

To enable publication, set the repository's **Settings > Pages > Build and
deployment > Source** to **GitHub Actions**. The report is visible to anyone
who can access the Pages site, so do not include sensitive data in tests.
GitHub Pages availability depends on the repository's plan and visibility.

To generate the same HTML report locally, install the development dependencies
and run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest tests -v --html=site/index.html --self-contained-html
```

Open `site/index.html` in a browser. These packages are only needed for HTML
reporting; the standard `unittest` commands above do not require them.

## Project structure

- `src/browser/`: WebDriver setup and Selenium helpers.
- `src/config/`: search and export settings.
- `src/pages/`: page objects and locators.
- `src/scrapers/`: scraper entry points.
- `tests/`: unit tests with mocked browser and workbook dependencies.

## Recommended VS Code extensions

- [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python):
  select an interpreter, run and debug code, and use the Testing view.
- [Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance):
  Python completions and diagnostics.
- [Excel Viewer](https://marketplace.visualstudio.com/items?itemName=GrapeCity.gc-excelviewer)
  (optional): inspect exported workbooks in VS Code.
