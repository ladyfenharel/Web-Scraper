import argparse
from scrape import setup_driver, fetch_ao3_works

def main():
    parser = argparse.ArgumentParser(description="Scrape AO3 bookmarks.")
    parser.add_argument("username", help="The AO3 username to scrape.")
    parser.add_argument("--visible", action="store_true", help="Run browser in visible mode.")
    args = parser.parse_args()

    driver = setup_driver(not args.visible)
    bookmarks = fetch_ao3_works(driver, args.username)
    driver.quit()

    if bookmarks:
        for bookmark in bookmarks:
            print(f"Title: {bookmark['title']}")
            print(f"Author: {bookmark['author']}")
            print(f"Fandom: {bookmark['fandom']}")
            print(f"Pairings: {bookmark['pairings']}")
            print(f"Tags: {bookmark['tags']}")
            print(f"Description: {bookmark['description']}")
            print(f"Ratings: {bookmark['ratings']}")
            print(f"Warnings: {bookmark['warnings']}")
            print(f"Categories: {bookmark['categories']}")
            print("-" * 20)
    else:
        print("No bookmarks found or an error occurred.")

if __name__ == "__main__":
    main()
