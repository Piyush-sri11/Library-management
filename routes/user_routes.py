from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt, JWTManager
from models import db, User
from schemas.user_schema import UserSchema

user_blueprint = Blueprint('user', __name__)
user_schema = UserSchema()
jwt = JWTManager()

revoked_tokens = set()

@user_blueprint.route('/register', methods=['POST'])
def register():
    data = request.json
    errors = user_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already exists"}), 400
    
    hashed_password = generate_password_hash(data['password'])
    user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        phone_number=data['phone_number'],
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201

@user_blueprint.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.user_id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid email or password"}), 401

@user_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    data= request.json
    print(data)
    jti = get_jwt()["jti"]
    revoked_tokens.add(jti)
    print(revoked_tokens)
    return jsonify({"message": "Logged out successfully"}), 200

@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in revoked_tokens