# API Documentation

## User Routes

### Register User

- URL: `/users/register`
- Method: `POST`
- Description: Register a new user.
- Request Body:
  {
    "first_name": "string",
    "last_name": "string",
    "email": "string",
    "phone_number": "string",
    "password": "string"
  }
- Responses:
  - `201 Created`: User registered successfully.
  - `400 Bad Request`: Validation errors or email already exists.

### Login User

- URL: `/users/login`
- Method: `POST`
- Description: Login a user.
- Request Body:
  {
    "email": "string",
    "password": "string"
  }
- Responses:
  - `200 OK`: Returns a JWT token.
  - `401 Unauthorized`: Invalid email or password.

### Logout User

- URL: `/users/logout`
- Method: `POST`
- Description: Logout a user.
- Headers: `Authorization: Bearer <JWT>`
- Responses:
  - `200 OK`: User logged out successfully.

## Book Routes

### Add Book

- URL: `/books/`
- Method: `POST`
- Description: Add a new book.
- Request Body:
  {
    "title": "string",
    "author": "string",
    "quantity": "integer"
  }
- Responses:
  - `201 Created`: Book added successfully.
  - `400 Bad Request`: Validation errors.

### Get Books

- URL: `/books/`
- Method: `GET`
- Description: Get a list of books with pagination.
- Query Parameters:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 3)
- Responses:
  - `200 OK`: Returns a list of books with pagination details.
  - `404 Not Found`: No books found.

### Get Book

- URL: `/books/<int:book_id>`
- Method: `GET`
- Description: Get details of a specific book.
- Responses:
  - `200 OK`: Returns book details.
  - `404 Not Found`: Book not found.

### Update Book

- URL: `/books/<int:book_id>`
- Method: `PUT`
- Description: Update details of a specific book.
- Request Body:
  {
    "title": "string",
    "author": "string",
    "quantity": "integer"
  }
- Responses:
  - `200 OK`: Book updated successfully.
  - `404 Not Found`: Book not found.

### Patch Book

- URL: `/books/<int:book_id>`
- Method: `PATCH`
- Description: Partially update details of a specific book.
- Request Body: Partial book details.
- Responses:
  - `200 OK`: Book updated successfully.
  - `404 Not Found`: Book not found.

### Delete Book

- URL: `/books/<int:book_id>`
- Method: `DELETE`
- Description: Delete a specific book.
- Responses:
  - `200 OK`: Book deleted successfully.
  - `404 Not Found`: Book not found.

## Issuance Routes

### Issue Book

- URL: `/issuances/issue`
- Method: `POST`
- Description: Issue a book to a user.
- Request Body:
  {
    "book_id": "integer",
    "user_id": "integer",
    "issue_date": "YYYY-MM-DD",
    "return_date": "YYYY-MM-DD"
  }
- Responses:
  - `201 Created`: Book issued successfully.
  - `400 Bad Request`: Validation errors or book not available.

### Return Book

- URL: `/issuances/return/<int:issue_id>`
- Method: `POST`
- Description: Return an issued book.
- Responses:
  - `200 OK`: Book returned successfully.
  - `404 Not Found`: Issue record not found.

### Extend Return Date

- URL: `/issuances/extend/<int:issue_id>`
- Method: `POST`
- Description: Extend the return date of an issued book.
- Request Body:
  {
    "return_date": "YYYY-MM-DD"
  }
- Responses:
  - `200 OK`: Return date extended successfully.
  - `404 Not Found`: Issue record not found.

### Get Overdue Issues

- URL: `/issuances/overdue`
- Method: `GET`
- Description: Get a list of overdue issues.
- Responses:
  - `200 OK`: Returns a list of overdue issues.
  - `404 Not Found`: No overdue issues found.

### Get User Issues

- URL: `/issuances/user/<int:user_id>`
- Method: `GET`
- Description: Get a list of issues for a specific user with pagination.
- Query Parameters:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 3)
- Responses:
  - `200 OK`: Returns a list of user issues with pagination details.
  - `404 Not Found`: No issue records found for the user.

### Get Book Issues

- URL: `/issuances/book/<int:book_id>`
- Method: `GET`
- Description: Get a list of issues for a specific book with pagination.
- Query Parameters:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 3)
- Responses:
  - `200 OK`: Returns a list of book issues with pagination details.
  - `404 Not Found`: No issue records found for the book.

### Get Issue

- URL: `/issuances/<int:issue_id>`
- Method: `GET`
- Description: Get details of a specific issue.
- Responses:
  - `200 OK`: Returns issue details.
  - `404 Not Found`: Issue record not found.

### Get Issues

- URL: `/issuances/`
- Method: `GET`
- Description: Get a list of all issues with pagination.
- Query Parameters:
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 3)
- Responses:
  - `200 OK`: Returns a list of issues with pagination details.
  - `404 Not Found`: No issues found.

## Home Route

### Home

- URL: `/`
- Method: `GET`
- Description: Home route.
- Responses:
  - `200 OK`: Returns a welcome message.