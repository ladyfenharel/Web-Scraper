from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from scraper.utils import extract_bookmark_data
from database import db, models
from sqlalchemy.orm import Session
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

def user_exists(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str):
    db_user = models.User(username=username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def fetch_ao3_bookmarks(username, visible=False):
    """Fetches and extracts data from AO3 bookmarks and stores them in the database."""
    url = f"https://archiveofourown.org/users/{username}/bookmarks"
    logging.info(f"Fetching bookmarks from: {url}")
    driver = setup_driver(visible)
    try:
        driver.get(url)
        accept_terms(driver)
        bookmark_elements = get_bookmark_elements(driver)
        bookmarks = [extract_bookmark_data(el) for el in bookmark_elements]

        database_generator = db.get_db() # get the generator.
        database = next(database_generator) # get the session.
        try:
            user = user_exists(database, username)
            if not user:
                user = create_user(database, username)
            for bookmark_data in bookmarks:
                db_bookmark = models.Bookmark(
                    title=bookmark_data['title'],
                    author=bookmark_data['author'],
                    fandom=bookmark_data['fandom'],
                    pairings=bookmark_data['pairings'],
                    tags=bookmark_data['tags'],
                    characters=bookmark_data['characters'],
                    description=bookmark_data['description'],
                    ratings=bookmark_data['ratings'],
                    warnings=bookmark_data['warnings'],
                    categories=bookmark_data['categories'],
                    user_id=user.id
                )
                database.add(db_bookmark)
            database.commit()
        finally:
            next(database_generator, None) #close the database.
        return bookmarks
    except Exception as e:
        logging.error(f"Error fetching bookmarks: {e}")
        return None
    finally:
        driver.quit()
