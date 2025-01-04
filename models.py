from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Book(db.Model):
    __tablename__ = "books"

    book_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    late_fee = db.Column(db.Float, nullable=False)  # Late fee per day

    def __repr__(self):
        return f"<Book {self.title}>"

class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)  # Store hashed passwords for security

    def __repr__(self):
        return f"<User {self.email}>"

class Issue(db.Model):
    __tablename__ = "issues"

    ISSUE_STATUSES = ["issued", "returned", "overdue"]

    issue_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    actual_return_date = db.Column(db.Date)
    late_fine = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(10), default="issued", nullable=False)

    @validates("status")
    def validate_status(self, key, status):
        if status not in self.ISSUE_STATUSES:
            raise ValueError(f"Invalid status '{status}'. Must be one of {self.ISSUE_STATUSES}.")
        return status

    def __repr__(self):
        return f"<Issue {self.issue_id} - Book {self.book_id} User {self.user_id}>"
