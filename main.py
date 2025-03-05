import argparse
from scraper.scrape import fetch_ao3_bookmarks
from database.db import init_db
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Scrape and store AO3 bookmarks.")
    parser.add_argument("username", help="The AO3 username to scrape.")
    parser.add_argument("--visible", action="store_true", help="Run browser in visible mode.")
    args = parser.parse_args()

    try:
        init_db()  # Initialize the database
        logging.info("Database initialized.")
        fetch_ao3_bookmarks(args.username)  # Scrape and store bookmarks
        logging.info(f"Bookmarks for {args.username} scraped and stored successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
