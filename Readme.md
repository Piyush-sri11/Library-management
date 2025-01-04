# Library Management System

## Project Description

This project is a library management system that allows users to register, login, and manage books. Users can issue and return books, and the system keeps track of overdue issues. The project includes APIs for user management, book management, and issuance management.

## How to Run

1. Clone the repository:
    ```bash
   git clone https://github.com/Piyush-sri11/Library-management.git
   
   ```
2.2. Set up a virtual environment:
   ```bash
   virtualenv venv
   ```   

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up config variables in ```bash config.py``` file:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'super-secret'  # Change this in your code

4. Run the application:
```bash
   python app.py
   ```

5. Access the application:
   Open your browser and go to `http://localhost:5000`

## How to Reset Database

1. Reset the db
   ```bash
   flask reset-db
   ```

## API documentation
    The API documentation can be accessed in the file
    - `Api_doc.md`
    - `library-management.postman_collection.json`


## Postman Collection 
  Run  to perform test on the server
  `https://go.postman.co/workspace/6e8936c1-b64b-4bfc-8794-698c89f45148/collection/38345023-b1e52c95-3ab0-427d-a850-ddeda9120834`



