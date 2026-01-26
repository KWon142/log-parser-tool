import re
from playwright.sync_api import Page, Locator

class BookstorePage:
    def __init__(self, page:Page):
        self.page = page
        self.title_input = page.get_by_role("textbox", name="Book Title") # get by type and content in element
        self.author_input = page.get_by_role("textbox", name="Author")
        self.price_input = page.get_by_placeholder("Price") # get by name of placholder
        self.add_book_input = page.get_by_role("button", name=re.compile("Add Book", re.IGNORECASE)) 
        
        self.error_message = page.locator("#error-message")

        self.saved_title = ""
        self.saved_author = ""
        self.saved_price = ""
        self.full_text = ""


    def enter_title(self, title: str):
        self.saved_title = title
        self.title_input.fill(title)

    def enter_author(self, author: str):
        self.saved_author = author
        self.author_input.fill(author)

    def enter_price(self, price: str):
        self.saved_price = price
        self.price_input.fill(price)

    def click_add(self):
        self.full_text = f"{self.saved_title} by {self.saved_author} ({self.saved_price})"
        self.add_book_input.click()
        
    def fill_book_details(self, title: str, author: str, price: int):
        self.title_input.fill(title)
        self.author_input.fill(author)
        self.price_input.fill(price)
        self.click_add()
        
    def new_book_locator(self)->Locator:
        return self.page.get_by_text(self.full_text) 
    
    def error_message_locator(self)->Locator:
        return self.error_message



    