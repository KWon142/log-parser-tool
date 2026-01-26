import re
import pytest
from playwright.sync_api import Page, expect
from pages.index_page import BookstorePage
import random
import time

@pytest.fixture(scope="function", autouse=True)
def before_each_after_each(page: Page):
    
    print("\nbefore the test runs")
    
    # Go to the starting url before each test.
    page.goto("file:///home/quanquan/Documents/newProject/test-project/tests/learning-fastAPI/frontend/index.html")
    
    yield

    print("\n after the test runs")

def test_positive_case(page: Page)->None:
    # author = "Kwon Pham %d" % random.randint(1,50)
    author = f"Kwon {int(time.time())}"
    index_page = BookstorePage(page)
    index_page.enter_author(author)
    index_page.enter_title("28 years later")
    index_page.enter_price("99.99")

    index_page.click_add()

    expect(index_page.error_message_locator()).to_be_hidden()
    expect(index_page.new_book_locator()).to_be_visible()

def test_negative_case(page: Page)->None:
    index_page = BookstorePage(page)
    index_page.enter_author("Quan Pham")
    index_page.enter_title("Harry Potter")
    index_page.enter_price("")
                           
    index_page.click_add()
    
    expect(index_page.error_message_locator()).to_be_visible()                       
    