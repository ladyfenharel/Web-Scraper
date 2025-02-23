from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import argparse

def setup_driver(headless=True):
    """Sets up the Chrome WebDriver."""
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)

def accept_terms(driver):
    """Finds and checks the required checkboxes, then clicks the 'I agree' button."""
    try:
        # Checkbox 1
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tos_agree")))
        checkbox1 = driver.find_element(By.ID, "tos_agree")
        print("Checkbox 1 found and clickable") #debug
        checkbox1.click()
        print("Checkbox 1 clicked") #debug

        # Checkbox 2
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "data_processing_agree")))
        checkbox2 = driver.find_element(By.ID, "data_processing_agree")
        print("Checkbox 2 found and clickable") #debug
        checkbox2.click()
        print("Checkbox 2 clicked") #debug

        # Agree Button
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accept_tos")))
        agree_button = driver.find_element(By.ID, "accept_tos")
        print("Agree button found and clickable") #debug
        agree_button.click()
        print("Agree button clicked") #debug

        print("Accepted AO3 terms.")
        WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, "accept_tos")))

    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error in accept_terms: {e}")
    except Exception as e:
        print(f"Unexpected Error in accept_terms: {e}")

def get_bookmark_elements(driver):
    """Retrieves all bookmark elements from the page."""
    try:
        # Wait for core element to load
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bookmark.blurb.group")))
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".bookmark.blurb.group")))
        return driver.find_elements(By.CSS_SELECTOR, ".bookmark.blurb.group")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error getting bookmark elements: {e}")
        return []

def extract_element_text(element, selector):
    """Extracts the text content of an element using a CSS selector."""
    try:
        return element.find_element(By.CSS_SELECTOR, selector).text
    except NoSuchElementException:
        return None

def extract_title(bookmark_element):
    """Extracts the title from a bookmark element."""
    return extract_element_text(bookmark_element, "h4.heading a")

def extract_author(bookmark_element):
    """Extracts the author from a bookmark element."""
    return extract_element_text(bookmark_element, "a[rel='author']")

def extract_fandom(bookmark_element):
    """Extracts the fandom from a bookmark element."""
    return extract_element_text(bookmark_element, "h5.fandoms.heading a.tag")

def extract_pairings(bookmark_element):
    """Extracts pairings from a bookmark element."""
    pairings = []
    try:
        tags_list = bookmark_element.find_element(By.CSS_SELECTOR, "ul.tags.commas")
        relationship_tags = tags_list.find_elements(By.CSS_SELECTOR, "li.relationships a.tag")
        pairings = [tag.text for tag in relationship_tags]
    except NoSuchElementException:
        pass
    return pairings

def extract_tags(bookmark_element):
    """Extracts tags from a bookmark element."""
    tags = []
    try:
        tags_list = bookmark_element.find_element(By.CSS_SELECTOR, "ul.tags.commas")
        freeform_tags = tags_list.find_elements(By.CSS_SELECTOR, "li.freeforms a.tag")
        tags = [tag.text for tag in freeform_tags]
    except NoSuchElementException:
        pass
    return tags

def extract_characters(bookmark_element):
    """Extracts Characters from a bookmark element."""
    characters = []
    try:
        tags_list = bookmark_element.find_element(By.CSS_SELECTOR, "ul.tags.commas")
        character_tags = tags_list.find_elements(By.CSS_SELECTOR, "li.characters a.tag")
        characters = [tag.text for tag in character_tags]
    except NoSuchElementException:
        pass
    return characters

def extract_description(bookmark_element):
    """Extracts description from a bookmark element."""
    return extract_element_text(bookmark_element, ".userstuff")

def extract_ratings(bookmark_element):
    """Extracts ratings from a bookmark element."""
    ratings = []
    rating_elements = bookmark_element.find_elements(By.CSS_SELECTOR, "ul.required-tags span[class^='rating-']")
    for rating_element in rating_elements:
        ratings.append(rating_element.get_attribute('title'))
    return ratings

def extract_warnings(bookmark_element):
    """Extracts warnings from a bookmark element."""
    warnings = []
    warning_elements = bookmark_element.find_elements(By.CSS_SELECTOR, "ul.required-tags span[class^='warning-']")
    for warning_element in warning_elements:
        warnings.append(warning_element.get_attribute('title'))
    return warnings

def extract_categories(bookmark_element):
    """Extracts categories from a bookmark element."""
    categories = []
    category_elements = bookmark_element.find_elements(By.CSS_SELECTOR, "ul.required-tags span[class^='category-']")
    for category_element in category_elements:
        categories.append(category_element.get_attribute('title'))
    return categories

def extract_bookmark_data(bookmark_element):
    """Extracts all relevant data from a bookmark element."""
    title = extract_title(bookmark_element)
    author = extract_author(bookmark_element)
    fandom = extract_fandom(bookmark_element)
    pairings = extract_pairings(bookmark_element)
    tags = extract_tags(bookmark_element)
    characters = extract_characters(bookmark_element)
    description = extract_description(bookmark_element)
    ratings = extract_ratings(bookmark_element)
    warnings = extract_warnings(bookmark_element)
    categories = extract_categories(bookmark_element)
    return {"title": title, "author": author, "fandom": fandom, "pairings": pairings, "tags": tags, "characters": characters, "description": description, "ratings": ratings, "warnings": warnings, "categories": categories}

def fetch_ao3_works(driver, username):
    """Fetches and extracts data from AO3 bookmarks."""
    url = f"https://archiveofourown.org/users/{username}/bookmarks"
    print(f"Fetching AO3 bookmarks from: {url}")
    driver.get(url)
    accept_terms(driver)
    bookmark_elements = get_bookmark_elements(driver)
    bookmarks_data = [extract_bookmark_data(element) for element in bookmark_elements]
    return bookmarks_data

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