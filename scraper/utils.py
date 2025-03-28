from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

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