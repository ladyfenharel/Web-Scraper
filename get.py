from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def setup_driver():
    """Set up Chrome WebDriver with the correct options."""
    options = Options()
    options.add_argument("--headless=new")  # Remove this if you want to see the browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    service = Service("/usr/local/bin/chromedriver")  # Update with the actual path to your ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def accept_terms(driver):
    """Finds and checks the required checkboxes, then clicks the 'I agree' button."""
    try:
        time.sleep(3)  # Wait for the pop-up to load

        # Check the checkboxes
        checkbox1 = driver.find_element(By.ID, "tos_agree")
        checkbox2 = driver.find_element(By.ID, "data_processing_agree")
        driver.execute_script("arguments[0].click();", checkbox1)
        driver.execute_script("arguments[0].click();", checkbox2)
        time.sleep(1)  # Wait for button activation

        # Click the "I agree" button
        agree_button = driver.find_element(By.ID, "accept_tos")
        driver.execute_script("arguments[0].click();", agree_button)

        print("Accepted AO3 terms.")
        time.sleep(2)  # Wait for the page to reload
    except Exception as e:
        print("No agreement pop-up found or error clicking it:", e)

def fetch_ao3_works(driver, username):
    """Fetches bookmarks from AO3 under a given tag."""
    url = f"https://archiveofourown.org/users/{username}/bookmarks"
    print(f"Fetching AO3 bookmarks from: {url}")
    
    driver.get(url)
    accept_terms(driver)  # Handle the pop-up if present

    time.sleep(3)  # Allow page to load
    works = driver.find_elements(By.CSS_SELECTOR, ".bookmark.blurb.group")  # Get works list

    if works:
        print(f"Found {len(works)} bookmarks on the page.")
        for i, work in enumerate(works[:5]):  # Print first 5 work titles
            title = work.find_element(By.CSS_SELECTOR, "h4.heading a").text
            print(f"{i+1}. {title}")
    else:
        print("No bookmarks found.")

# Example usage
driver = setup_driver()
fetch_ao3_works(driver, "ladyfenharel")  # Replace with your tag

driver.quit()  # Close browser when done
