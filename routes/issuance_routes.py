from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Issue, Book
from schemas.issuance_schema import IssueSchema
from datetime import datetime, timedelta

issuance_blueprint = Blueprint('issuance', __name__)
issue_schema = IssueSchema()
issues_schema = IssueSchema(many=True)

@issuance_blueprint.route('/issue', methods=['POST'])
# @jwt_required()
def issue_book():
    data = request.json
    errors = issue_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    book = Book.query.get(data['book_id'])
    if not book or book.quantity <= 0:
        return jsonify({"message": "Book not available"}), 400
    
    #return date should be after issue date
    if datetime.strptime(data['return_date'], "%Y-%m-%d") <= datetime.strptime(data['issue_date'], "%Y-%m-%d"):
        return jsonify({"message": "Return date must be after issue date"}), 400

    issue = Issue(
        book_id=data['book_id'],
        # user_id=get_jwt_identity(),
        user_id=data["user_id"],
        issue_date=datetime.strptime(data['issue_date'], "%Y-%m-%d"),
        return_date=datetime.strptime(data['return_date'], "%Y-%m-%d"),
        status='issued'
    )
    book.quantity -= 1
    db.session.add(issue)
    db.session.commit()
    return jsonify(issue_schema.dump(issue)), 201

@issuance_blueprint.route('/return/<int:issue_id>', methods=['POST'])
# @jwt_required()
def return_book(issue_id):
    issue = Issue.query.get(issue_id)
    if not issue or issue.status == 'returned':
        return jsonify({"message": "Invalid issue record"}), 400

    issue.actual_return_date = datetime.utcnow()
    book = Book.query.get(issue.book_id)
    if issue.actual_return_date.date() > issue.return_date:
        late_days = (issue.actual_return_date - issue.return_date).days
        issue.late_fine = late_days * book.late_fee

    issue.status = 'returned'
    book.quantity += 1
    db.session.commit()
    return jsonify(issue_schema.dump(issue)), 200


@issuance_blueprint.route('/extend/<int:issue_id>', methods=['POST'])
# @jwt_required()
def extend_return(issue_id):
    data = request.json
    issue = Issue.query.get(issue_id)
    if not issue or issue.status != 'issued':
        return jsonify({"message": "Invalid issue record"}), 400

    new_return_date = datetime.strptime(data['return_date'], "%Y-%m-%d")
    if new_return_date.date() <= issue.return_date:
        return jsonify({"message": "New return date must be after the current return date"}), 400

    issue.return_date = new_return_date
    db.session.commit()
    return jsonify(issue_schema.dump(issue)), 200


@issuance_blueprint.route('/overdue', methods=['GET'])
# @jwt_required()   
def get_overdue_issues():
    overdue_issues = Issue.query.filter(Issue.return_date < datetime.utcnow(), Issue.status == 'issued').all()
    return jsonify(issues_schema.dump(overdue_issues)), 200

@issuance_blueprint.route('/user/<int:user_id>', methods=['GET'])
# @jwt_required()
def get_user_issues(user_id):
    user_issues = Issue.query.filter_by(user_id=user_id).all()
    return jsonify(issues_schema.dump(user_issues)), 200

@issuance_blueprint.route('/book/<int:book_id>', methods=['GET'])
# @jwt_required()
def get_book_issues(book_id):
    book_issues = Issue.query.filter_by(book_id=book_id).all()
    return jsonify(issues_schema.dump(book_issues)), 200

@issuance_blueprint.route('/<int:issue_id>', methods=['GET'])
# @jwt_required()
def get_issue(issue_id):
    issue = Issue.query.get(issue_id)
    if not issue:
        return jsonify({"message": "Issue record not found"}), 404
    return jsonify(issue_schema.dump(issue)), 200

@issuance_blueprint.route('/', methods=['GET'])
# @jwt_required()
def get_issues():
    issues = Issue.query.all()
    return jsonify(issues_schema.dump(issues)), 200