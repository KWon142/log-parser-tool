from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 1. Define the Data Model
class Book(BaseModel): 
    id: int
    title: str
    author: str
    price: float

# 2. Mock Database
books_db = [
    {"id": 1, "title": "1984", "author": "George Orwell", "price": 9.99},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "price": 7.99},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "price": 10.99},
    {"id": 4, "title": "Clean Code", "author": "Robert C. Martin", "price": 45.00}
]

# 3. Routes (The Endpoints)
@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore API!"}

@app.get("/books/", response_model=List[Book])
def get_books():
    """
    Retrieve a list of all books in the database.
    """
    return books_db

@app.get("/books/{book_id}", response_model=Book)
def get_book_detail(book_id: int):
    """
    Retrieve a specific book by its ID. 
    Returns 404 if not found.
    """
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/", response_model=Book, status_code=201)
def create_book(book: Book):
    """
    Create a new book. 
    The book parameter is automatically validated against the Book model.
    """
    # Convert Pydantic model( .model_dump() ) to a dictionary
    new_book = book.model_dump()
    # Check for duplicate ID
    for book in books_db:
        if book["id"] == new_book["id"]:
            raise HTTPException(status_code=400, detail="Book ID already exists")
    books_db.append(new_book)
    return new_book




