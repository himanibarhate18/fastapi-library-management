# Library Management System REST API

## Project Overview

The Library Management System is a REST API developed using Python and FastAPI to manage library books, members, and borrowing activities. It uses PostgreSQL to store data, SQLAlchemy for database operations, and Pydantic for data validation.

The main objective of this project is to simplify library record management by providing APIs to add, view, update, and delete books, register members, and manage book borrowing and returning.

## Objectives

- Develop a REST API using FastAPI.
- Store and manage library data using PostgreSQL.
- Perform database operations using SQLAlchemy.
- Validate request data using Pydantic.
- Manage book availability during borrowing and returning.
- Test API endpoints using Swagger UI.

## Technologies Used

- **Python:** Programming language used to develop the application.
- **FastAPI:** Framework used to build REST API endpoints.
- **PostgreSQL:** Relational database used to store library information.
- **SQLAlchemy:** ORM used to interact with the database.
- **Pydantic:** Used to validate request data and structure API responses.
- **Uvicorn:** ASGI server used to run the FastAPI application.
- **Swagger UI:** Interactive interface used to test API endpoints.

## Features

- Add new books to the library.
- View all books.
- Retrieve book details by ID.
- Update book information.
- Delete books.
- Register library members.
- View all members.
- Retrieve member details by ID.
- Borrow available books.
- Return borrowed books.
- Maintain book availability counts.
- Validate incoming request data.
- Handle errors such as missing records, duplicate values, and unavailable books.

## Database Design

The project uses PostgreSQL with three main tables:

### 1. Books

Stores information about library books.

Fields include:
- `id`
- `title`
- `author`
- `isbn`
- `total_copies`
- `available_copies`

### 2. Members

Stores registered library member information.

Fields include:
- `id`
- `name`
- `email`

### 3. Borrow Records

Stores information about book borrowing and returning.

Fields include:
- `id`
- `book_id`
- `member_id`
- `borrow_date`
- `due_date`
- `return_date`
- `status`

The `book_id` and `member_id` fields connect borrowing records to books and members through foreign keys.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check whether the API is running |
| GET | `/books` | Retrieve all books |
| GET | `/books/{book_id}` | Retrieve a book by ID |
| POST | `/books` | Add a new book |
| PUT | `/books/{book_id}` | Update book details |
| DELETE | `/books/{book_id}` | Delete a book |
| GET | `/members` | Retrieve all members |
| GET | `/members/{member_id}` | Retrieve a member by ID |
| POST | `/members` | Register a new member |
| POST | `/borrow` | Borrow a book |
| POST | `/return/{record_id}` | Return a borrowed book |
| GET | `/borrow-records` | Retrieve borrowing records |

## Business Rules and Validation

- A book can be borrowed only when copies are available.
- Borrowing a book decreases its available copy count.
- Returning a book increases its available copy count.
- Book and member records must exist before borrowing.
- Duplicate ISBNs and member email addresses are rejected.
- Invalid input is handled through request validation.
- Missing records return appropriate HTTP errors.

## Installation and Setup

### Prerequisites

- Python installed
- PostgreSQL installed and running
- Visual Studio Code
- pip package manager

### Step 1: Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 3: Configure the Database

Create a PostgreSQL database named `library_db`.

Create a `.env` file in the project root containing your database connection string:

```text
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/library_db
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

**Security:** Never upload `.env` or publish your database password on GitHub.

### Step 4: Create Database Tables

Run:

```bash
python create_tables.py
```

The script should create the required database tables.

### Step 5: Start the API

Run:

```bash
python -m uvicorn main:app --reload
```

### Step 6: Open API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

Use Swagger UI to explore and test the available endpoints.

## API Testing

The API can be tested using Swagger UI at `/docs`.

Important tests include:

- Creating and retrieving a book.
- Updating book details.
- Registering and retrieving a member.
- Borrowing an available book.
- Returning a borrowed book.
- Checking unavailable-book handling.
- Testing invalid input.
- Testing missing records.
- Testing duplicate ISBNs and email addresses.

Expected HTTP responses depend on the endpoint and implementation, including success responses and validation or error responses.

## Project Structure

```text
fastapi-library-management/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── create_tables.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
```

The `.env` file is for local configuration only and must not be uploaded to GitHub.

## Future Enhancements

- Search books by title or author.
- Add pagination for large collections.
- Implement authentication and authorization.
- Add automated API tests.
- Add overdue-book tracking and reports.
- Deploy the API to a hosting platform.

## Conclusion

This project demonstrates the development of a REST API using FastAPI, integration with a PostgreSQL database, database operations through SQLAlchemy, and data validation using Pydantic. It provides a foundation for understanding backend development and database-driven applications.

## Author

**Himani Barhate**
