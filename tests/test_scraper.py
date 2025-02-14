import sys
import os
print("sys.path before:")
print(sys.path)

# Add this line (modified from before)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # CORRECTED LINE
print("\nsys.path after adding current dir:")
print(sys.path)

import pytest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from get import setup_driver, accept_terms, fetch_ao3_works  # Replace your_module

@pytest.fixture(scope="module")
def driver():
    """
    Fixture to set up and teardown a mock WebDriver instance for testing.
    Module-scoped to reuse the same driver instance for all tests in this module,
    improving test speed.
    """
    driver_instance = MockDriver()  # Use MockDriver instead of real setup_driver for unit tests
    yield driver_instance
    # No need to quit a MockDriver

def test_setup_driver():
    """Unit test to check if setup_driver returns a WebDriver instance."""
    driver_instance = setup_driver()
    assert isinstance(driver_instance, webdriver.Chrome)
    driver_instance.quit() # Need to quit even if we are also using mock driver for other tests to avoid resource leaks in actual runs

def test_accept_terms_popup_present(driver, capsys):
    """Unit test for accept_terms when the pop-up is present."""
    # Mock find_element to simulate pop-up elements being found
    checkbox_mock_1 = MockElement(tag_name='input', attributes={'id': 'tos_agree'})
    checkbox_mock_2 = MockElement(tag_name='input', attributes={'id': 'data_processing_agree'})
    agree_button_mock = MockElement(tag_name='button', attributes={'id': 'accept_tos'})

    with patch.object(driver, 'find_element', side_effect=lambda by, value: {
        "tos_agree": checkbox_mock_1,
        "data_processing_agree": checkbox_mock_2,
        "accept_tos": agree_button_mock
    }[value]): # Use a dictionary to map expected 'value' to mock elements
        accept_terms(driver)
    captured = capsys.readouterr()
    assert "Accepted AO3 terms." in captured.out

def test_accept_terms_popup_not_present(driver, capsys):
    """Unit test for accept_terms when the pop-up is NOT present."""
    # Mock find_element to raise an exception, simulating no pop-up
    with patch.object(driver, 'find_element', side_effect=Exception("No element found")):
        accept_terms(driver)
    captured = capsys.readouterr()
    assert "No agreement pop-up found" in captured.out

def test_fetch_ao3_works_bookmarks_found_multiple_titles(driver, capsys):
    """Unit test for fetch_ao3_works when bookmarks are found, testing multiple titles."""
    mock_works = [
        MockElement(tag_name='div', attributes={'class': 'bookmark blurb group'}, children=[
            MockElement(tag_name='h4', attributes={'class': 'heading'}, children=[
                MockElement(tag_name='a', text='Test Work Title 1')
            ]),
        ]),
        MockElement(tag_name='div', attributes={'class': 'bookmark blurb group'}, children=[
            MockElement(tag_name='h4', attributes={'class': 'heading'}, children=[
                MockElement(tag_name='a', text='Another Great Work Title')
            ]),
        ]),
        MockElement(tag_name='div', attributes={'class': 'bookmark blurb group'}, children=[
            MockElement(tag_name='h4', attributes={'class': 'heading'}, children=[
                MockElement(tag_name='a', text='Yet One More Title Here')
            ]),
        ]),
    ]
    with patch.object(driver, 'find_elements', return_value=mock_works):
        fetch_ao3_works(driver, "testuser")
    captured = capsys.readouterr()
    assert "Found 3 bookmarks" in captured.out
    assert "1. Test Work Title 1" in captured.out
    assert "2. Another Great Work Title" in captured.out
    assert "3. Yet One More Title Here" in captured.out

def test_fetch_ao3_works_bookmarks_found_less_than_5(driver, capsys):
    """Unit test for fetch_ao3_works when fewer than 5 bookmarks are found."""
    mock_works = [
        MockElement(tag_name='div', attributes={'class': 'bookmark blurb group'}, children=[
            MockElement(tag_name='h4', attributes={'class': 'heading'}, children=[
                MockElement(tag_name='a', text='Only One Bookmark')
            ]),
        ]),
    ]
    with patch.object(driver, 'find_elements', return_value=mock_works):
        fetch_ao3_works(driver, "testuser")
    captured = capsys.readouterr()
    assert "Found 1 bookmarks" in captured.out
    assert "1. Only One Bookmark" in captured.out
    assert "2." not in captured.out  # Ensure it doesn't try to print a 2nd title if none exists

def test_fetch_ao3_works_no_bookmarks_found(driver, capsys):
    """Unit test for fetch_ao3_works when no bookmarks are found."""
    with patch.object(driver, 'find_elements', return_value=[]):
        fetch_ao3_works(driver, "testuser")
    captured = capsys.readouterr()
    assert "No bookmarks found." in captured.out


class MockElement:
    """
    A simplified mock class to simulate Selenium WebElement behavior for testing purposes.
    This mock focuses on the functionalities used in the tested code (finding elements,
    getting text, clicking, getting attributes). It's not a complete WebElement replacement.
    """
    def __init__(self, tag_name, text='', attributes=None, children=None):
        """
        Initializes a MockElement.

        Args:
            tag_name (str): The tag name of the HTML element (e.g., 'div', 'a', 'button').
            text (str, optional): The text content of the element. Defaults to ''.
            attributes (dict, optional): A dictionary of HTML attributes (e.g., {'class': 'heading', 'id': 'tos_agree'}). Defaults to None.
            children (list of MockElement, optional): A list of child MockElements. Defaults to None.
        """
        self.tag_name = tag_name
        self.text = text
        self.attributes = attributes or {}
        self.children = children or []

    def find_element(self, by, selector):
        """
        Mock implementation of find_element.  Simplistically searches children based on selector value.
        For more complex selectors, this would need to be expanded.

        Args:
            by (By):  Selenium By class (not actually used in this simplified mock, but kept for API compatibility).
            selector (str): The selector (e.g., CSS selector, ID).

        Returns:
            MockElement: The found MockElement if a child matches the selector (based on attribute values).
        Raises:
            Exception: if Mock Element not found.
        """
        if self.children:
            for child in self.children:
                for attr_value in child.attributes.values():
                    if selector == attr_value: # Basic attribute value matching
                        return child
        raise Exception(f"Mock Element with selector '{selector}' not found in children of '{self.tag_name}'")

    def find_elements(self, by, selector):
        """
        Mock implementation of find_elements.  Simplistically searches children based on selector value.

        Args:
            by (By): Selenium By class (not actually used, for API compatibility).
            selector (str): The selector.

        Returns:
            list of MockElement: A list of MockElements whose attributes contain the selector value.
        """
        found_elements = []
        if self.children:
            for child in self.children:
                for attr_value in child.attributes.values():
                    if selector == attr_value: # Basic attribute value matching
                        found_elements.append(child)
        return found_elements

    def get_attribute(self, name):
        """
        Mock implementation of get_attribute.

        Args:
            name (str): The attribute name.

        Returns:
            str or None: The attribute value if found, None otherwise.
        """
        return self.attributes.get(name)

    @property
    def text(self):
        """Getter for text property."""
        return self._text

    @text.setter
    def text(self, value):
        """Setter for text property."""
        self._text = value

    def click(self):
        """Mock implementation of click."""
        print(f"Mock Element '{self.tag_name}' clicked.")

    def send_keys(self, value):
        """Mock implementation of send_keys."""
        print(f"Mock Element '{self.tag_name}' sending keys: {value}")

    def is_displayed(self):
        """Mock implementation of is_displayed.  Always returns True for simplicity in mocks."""
        return True

    @property
    def parent(self):
        """Mock implementation of parent property. Always returns None for simplicity here."""
        return None


class MockDriver:
    """
    A mock class to simulate the Selenium WebDriver for testing purposes.
    This mock focuses on the methods used in the tested code (get, find_element, find_elements, execute_script, quit).
    """
    def __init__(self):
        """Initializes MockDriver. Keeps track of 'current_url'."""
        self.current_url = None

    def get(self, url):
        """Mock implementation of get.  Sets the 'current_url'."""
        print(f"MockDriver navigating to: {url}")
        self.current_url = url

    def find_element(self, by, value):
        """
        Mock implementation of find_element.  Needs to be patched/mocked in tests to return specific MockElements.
        This default implementation raises an exception to indicate it needs to be mocked in each test.
        """
        raise NotImplementedError("find_element needs to be mocked in test")

    def find_elements(self, by, selector):
        """
        Mock implementation of find_elements. Needs to be patched/mocked in tests to return lists of MockElements.
        This default implementation returns an empty list.
        """
        return [] # Default to no elements found if not mocked in the test

    def execute_script(self, script, element):
        """Mock implementation of execute_script. Prints the script for verification."""
        print(f"MockDriver executing script: {script} on element '{element.tag_name}'")
        element.click() # Simulate click for scripts that click elements

    def quit(self):
        """Mock implementation of quit.  Prints a message."""
        print("MockDriver quit.")