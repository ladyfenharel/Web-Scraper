import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from unittest.mock import patch, MagicMock
from selenium import webdriver
from selenium.webdriver.common.by import By
from get import (
    setup_driver,
    accept_terms,
    fetch_ao3_works,
    extract_author,
    extract_fandom,
    extract_pairings,
    extract_tags,
    extract_characters,
    extract_ratings,
    extract_warnings,
    extract_categories,
    extract_bookmark_data,
    get_bookmark_elements,
)

@pytest.fixture(scope="module")
def driver():
    driver_instance = MockDriver()
    yield driver_instance

def test_setup_driver():
    driver_instance = setup_driver()
    assert isinstance(driver_instance, webdriver.Chrome)
    driver_instance.quit()

def test_accept_terms_popup_present(driver, capsys):
    checkbox_mock_1 = MockElement(tag_name='input', attributes={'id': 'tos_agree'})
    checkbox_mock_2 = MockElement(tag_name='input', attributes={'id': 'data_processing_agree'})
    agree_button_mock = MockElement(tag_name='button', attributes={'id': 'accept_tos'})

    with patch.object(driver, 'find_element', side_effect=lambda by, value: {
        "tos_agree": checkbox_mock_1,
        "data_processing_agree": checkbox_mock_2,
        "accept_tos": agree_button_mock
    }[value]):
        accept_terms(driver)
    captured = capsys.readouterr()
    assert "Accepted AO3 terms." in captured.out

def test_accept_terms_popup_not_present(driver, capsys):
    with patch("get.accept_terms", MagicMock()):
        with patch.object(driver, 'find_element', side_effect=Exception("No element found")):
            accept_terms(driver)
        captured = capsys.readouterr()
        assert "No agreement pop-up found" in captured.out

def test_fetch_ao3_works_bookmarks_found_multiple_titles(driver, capsys):
    mock_bookmarks = [
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
    ]
    with patch("get.get_bookmark_elements", return_value=mock_bookmarks):
        with patch("get.extract_bookmark_data", side_effect=lambda element: {
            "title": element.find_element(By.TAG_NAME, "a").text,
            "author": "Test Author",
            "fandom": "Test Fandom",
            "pairings": [],
            "tags": [],
            "characters": [],
            "description": "",
            "ratings": [],
            "warnings": [],
            "categories": [],
        }):
            bookmarks = fetch_ao3_works(driver, "testuser")
            assert len(bookmarks) == 2
            assert bookmarks[0]["title"] == "Test Work Title 1"
            assert bookmarks[1]["title"] == "Another Great Work Title"

def test_fetch_ao3_works_no_bookmarks_found(driver, capsys):
    with patch("get.accept_terms", MagicMock()):
        with patch("get.get_bookmark_elements", return_value=[]):
            fetch_ao3_works(driver, "testuser")
        captured = capsys.readouterr()
        assert "No bookmarks found or an error occurred." in captured.out

def test_extract_author(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='a', attributes={'rel': 'author'}, text='Test Author')])
    assert extract_author(bookmark_element) == 'Test Author'

def test_extract_fandom(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='h5', attributes={'class': 'fandoms heading'}, children=[MockElement(tag_name='a', attributes={'class': 'tag'}, text='Test Fandom')])])
    assert extract_fandom(bookmark_element) == 'Test Fandom'

def test_extract_pairings(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'tags commas'}, children=[MockElement(tag_name='li', attributes={'class': 'relationships'}, children=[MockElement(tag_name='a', attributes={'class': 'tag'}, text='Test Pairing')])])])
    assert extract_pairings(bookmark_element) == ['Test Pairing']

def test_extract_tags(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'tags commas'}, children=[MockElement(tag_name='li', attributes={'class': 'freeforms'}, children=[MockElement(tag_name='a', attributes={'class': 'tag'}, text='Test Tag')])])])
    assert extract_tags(bookmark_element) == ['Test Tag']

def test_extract_characters(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'tags commas'}, children=[MockElement(tag_name='li', attributes={'class': 'characters'}, children=[MockElement(tag_name='a', attributes={'class': 'tag'}, text='Test Character')])])])
    assert extract_characters(bookmark_element) == ['Test Character']

def test_extract_ratings(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'required-tags'}, children=[MockElement(tag_name='span', attributes={'class': 'rating-explicit', 'title': 'Explicit'})])])
    assert extract_ratings(bookmark_element) == ['Explicit']

def test_extract_warnings(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'required-tags'}, children=[MockElement(tag_name='span', attributes={'class': 'warning-choosenotto', 'title': 'Choose Not To Use Archive Warnings'})])])
    assert extract_warnings(bookmark_element) == ['Choose Not To Use Archive Warnings']

def test_extract_categories(driver):
    bookmark_element = MockElement(tag_name='div', children=[MockElement(tag_name='ul', attributes={'class': 'required-tags'}, children=[MockElement(tag_name='span', attributes={'class': 'category-het', 'title': 'F/M'})])])
    assert extract_categories(bookmark_element) == ['F/M']

class MockElement:
    def __init__(self, tag_name, text='', attributes=None, children=None):
        self.tag_name = tag_name
        self.text = text
        self.attributes = attributes or {}
        self.children = children or []

    def find_element(self, by, selector):
        if by == By.CSS_SELECTOR:
            parts = selector.split()
            current_elements = [self]
            for part in parts:
                next_elements = []
                for current_element in current_elements:
                    if current_element.children:
                        for child in current_element.children:
                            if self._matches_selector_part(child, part):
                                next_elements.append(child)
                current_elements = next_elements
            if current_elements:
                return current_elements[0]
            else:
                raise Exception(f"Mock Element with selector '{selector}' not found in children of '{self.tag_name}'")
        elif by == By.TAG_NAME:
            for child in self.children:
                if child.tag_name == selector:
                    return child
            raise Exception(f"Mock Element with tag_name '{selector}' not found in children of '{self.tag_name}'")
        else:
            if self.children:
                for child in self.children:
                    for attr_value in child.attributes.values():
                        if selector == attr_value:
                            return child
            raise Exception(f"Mock Element with selector '{selector}' not found in children of '{self.tag_name}'")

    def _matches_selector_part(self, element, part):
        if '.' in part:
            parts = part.split('.')
            tag_name = parts[0]
            class_names = parts[1:]
            if tag_name != '*' and tag_name != element.tag_name:
                return False
            for class_name in class_names:
                if class_name not in element.attributes.get('class', '').split():
                    return False
            return True
        elif '[' in part:
            tag_name, attribute_part = part.split('[')
            attribute_name, attribute_value = attribute_part[:-1].split('=')
            if tag_name != '*' and tag_name != element.tag_name:
                return False
            return element.attributes.get(attribute_name) == attribute_value.strip("'")
        else:
            return part == element.tag_name or part == '*'

    def find_elements(self, by, selector):
        found_elements = []
        if self.children:
            for child in self.children:
                if self._matches_selector_part(child, selector):
                    found_elements.append(child)
        return found_elements

    def get_attribute(self, name):
        return self.attributes.get(name)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def click(self):
        print(f"Mock Element '{self.tag_name}' clicked.")

    def send_keys(self, value):
        print(f"Mock Element '{self.tag_name}' sending keys: {value}")

    def is_displayed(self):
        return True

    @property
    def parent(self):
        return None

    def is_enabled(self):
        return True
    
class MockDriver:
    def __init__(self):
        self.elements = {}

    def find_element(self, by, value):
        if value in self.elements:
            return self.elements[value]
        raise Exception(f"Mock Driver: No element found for selector '{value}'")

    def find_elements(self, by, value):
        return [element for key, element in self.elements.items() if key == value]

    def quit(self):
        print("Mock Driver: Quit called.")

    def get(self, url):
        print(f"Mock Driver: Navigating to {url}")
