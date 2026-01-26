# 📚 Learning FastAPI - Bookstore Project

## 📂 Project Structure
```text
learning-fastAPI/
├── bookstore_db.py      # Backend Code (FastAPI Server & Mock Database)
├── frontend/            # User Interface folder
│   ├── my-index.html    # Practice UI file
│   └── draft.html       # Draft file
└── README.md            # Project documentation
```

## 🚀 Prerequisites
- Python 3.12+
- uv 

## 🛠️ Setup & Installation

1. Start the Backend (FastAPI)
The server handles data processing and provides API endpoints.
    1. Open your Terminal in the root directory learning-fastAPI.
   
    2. Install the required dependencies (if you haven't already):
        ```bash
        uv add fastapi
        ```
    3. Run the server using the following command:
        ```bash
        uv run fastapi dev bookstore_db.py
1. Launch the Frontend
The Frontend allows users to interact with the API to add and view books.

    **Recommended Method (To avoid CORS issues):**

    Open the project in VS Code.

    Install the Live Server extension (by Ritwick Dey).

    Right-click on frontend/index.html.

    Select "Open with Live Server".

    Simple Method:

    Navigate to the frontend folder and double-click index.html to open it in your browser.

## 📡 API Usage
This project provides the following key API endpoints (see /docs for full details):

- GET /books/: Retrieve a list of all books.

- POST /books/: Add a new book (Requires JSON body: title, author, year).

- GET /books/{book_id}: Retrieve details of a specific book.

- DELETE /books/{book_id}: Remove a book from the database.  