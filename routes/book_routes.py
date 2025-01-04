from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Book
from schemas.books_schema import BookSchema
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

book_blueprint = Blueprint('book', __name__)
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@book_blueprint.route('/', methods=['POST'])
# @jwt_required()
def add_book():
    data = request.json
    print(data)
    logging.debug(f"Received data: {data}") 
    errors = book_schema.validate(data)
    if errors:
        logging.debug(f"Validation errors: {errors}")  # Log validation errors
        return jsonify(errors), 400
    
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 201

@book_blueprint.route('/<int:book_id>', methods=['PUT'])
# @jwt_required()
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    data = request.json
    for key, value in data.items():
        setattr(book, key, value)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 200

@book_blueprint.route('/<int:book_id>', methods=['DELETE'])
# @jwt_required()
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"}), 200

@book_blueprint.route('/', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify(books_schema.dump(books)), 200

@book_blueprint.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    return jsonify(book_schema.dump(book)), 200

@book_blueprint.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q', '').strip()  # Get and strip whitespace from input
    if not query:
        return jsonify({"message": "Search query cannot be empty"}), 400

    # Perform case-insensitive search on title or author
    books = Book.query.filter(
        (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
    ).all()

    if not books:
        return jsonify({"message": "No books found matching the query"}), 404

    return jsonify(books_schema.dump(books)), 200

@book_blueprint.route('/<int:book_id>', methods=['PATCH'])
# @jwt_required()
def patch_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Book not found"}), 404
    
    data = request.json
    for key, value in data.items():
        if hasattr(book, key):
            setattr(book, key, value)
    db.session.commit()
    return jsonify(book_schema.dump(book)), 200
