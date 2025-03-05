# 📚 AO3 Bookmark Scraper 🔖

This Python script scrapes bookmark data from Archive of Our Own (AO3) for a specified user. It extracts information like work titles, authors, fandoms, pairings, tags, and more.

## ✨ Features

-   Fetches bookmark data from a given AO3 user's page 📖.
-   Extracts key metadata for each bookmarked work 🔍.
-   Handles AO3's terms of service agreement popup ✅.
-   Provides a clean, structured output of bookmark data 📊.

## ⚙️ Prerequisites

-   Python 3.6+
-   `selenium` library
-   A compatible web browser (Chrome, Firefox , etc.) and its corresponding WebDriver.

## ⬇️ Installation

1.  Clone the repository:

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  Install the required Python packages:

    ```bash
    pip install selenium
    ```

3.  Download the appropriate WebDriver for your browser and add it to your PATH or specify its location in the script.
    * Chrome: [ChromeDriver download](https://chromedriver.chromium.org/downloads)
    * Firefox: [GeckoDriver download](https://github.com/mozilla/geckodriver/releases)

## 🚀 Usage

1.  Run the script:

    ```bash
    python get.py [AO3 username]
    ```

    Replace `[AO3 username]` with the username of the AO3 user whose bookmarks you want to scrape.
    
2. Add `--visible` to the script if you prefer the WebDriver to not launch headless.

3.  The script will output the scraped bookmark data to the console 🖥️.

## 📝 Example

```bash
python get.py myAO3username
```

## 🧪 Testing

To run the unit tests:

```bash
pytest tests/test_scraper.py
```

## 📂 Project Structure
```bash
📦 AO3-Bookmark-Scraper
├── 📜 get.py                 # Main script for scraping AO3 bookmarks
├── 📂 tests
│   ├── ✅ test_scraper.py    # Unit tests for the scraping functionality
├── 📖 README.md              # Project documentation
```

## ⚠️ Notes
-   **Educational Purposes Only:** This script is provided for educational purposes, demonstrating web scraping techniques.
-   **Respect for Creative Rights:** The author of this script does not support the use of web scraping for AI training purposes. It is crucial to respect the creative rights of authors and adhere to the terms of service of websites.
-   Be mindful of AO3's terms of service and robots.txt.
-   The script may need to be updated if AO3's website structure changes.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a pull request.
