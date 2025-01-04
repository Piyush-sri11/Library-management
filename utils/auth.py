from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

def create_token(identity):
    token = create_access_token(identity=identity)
    return token