from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from utils import extract_bookmark_data

def setup_driver(headless=True):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)

def accept_terms(driver):
    """Handles AO3 Terms of Service popup."""
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "tos_agree"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "data_processing_agree"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accept_tos"))).click()
    except Exception:
        pass  # If elements aren't found, assume already accepted

def get_bookmark_elements(driver):
    """Retrieves all bookmark elements from the page."""
    return driver.find_elements(By.CSS_SELECTOR, ".bookmark.blurb.group")

def fetch_ao3_bookmarks(username):
    """Fetches and extracts data from AO3 bookmarks."""
    url = f"https://archiveofourown.org/users/{username}/bookmarks"
    driver = setup_driver()
    driver.get(url)
    accept_terms(driver)
    bookmarks = [extract_bookmark_data(el) for el in get_bookmark_elements(driver)]
    driver.quit()
    return bookmarks
