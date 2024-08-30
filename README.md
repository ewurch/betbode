# Football Odds Scraper

This project is a web scraper that fetches football match odds from the Oddspedia website using Selenium and BeautifulSoup. The scraped data is cached to reduce the number of requests to the website.

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4
- Geckodriver (for Firefox)
- Firefox browser

## Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/football-odds-scraper.git
    cd football-odds-scraper
    ```

2. **Install the required Python packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Download and install Geckodriver:**
    - For macOS:
        ```sh
        brew install geckodriver
        ```
    - For other operating systems, download from [Geckodriver releases](https://github.com/mozilla/geckodriver/releases) and follow the installation instructions.

## Usage

1. **Run the scraper:**
    ```sh
    python scraper.py
    ```

2. **Output:**
    The script will print the extracted match odds to the console.

## Configuration

- **Cache Duration:**
    The cache duration is set to 5 minutes by default. You can change this by modifying the `CACHE_DURATION` variable in `scraper.py`.

- **HTML File Path:**
    The HTML files are saved in the `html_cache` directory. You can change the path by modifying the `HTML_FILE_PATH` variable in `scraper.py`.

## Code Overview

- **fetch_html_with_selenium(url):**
    Fetches the HTML content of the given URL using Selenium and saves it to a file.

- **load_html_from_file(url):**
    Loads the HTML content from a cached file.

- **is_cache_valid(url):**
    Checks if the cached HTML file is still valid based on the cache duration.

- **scrape_matches():**
    Scrapes the match odds from the Oddspedia website and prints the extracted data.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.