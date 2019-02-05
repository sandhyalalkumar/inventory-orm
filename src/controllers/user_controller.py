import os
from flask import jsonify, Blueprint, request
from src.models import db
from src.models.user_model import User, UserSchema
from flask import current_app as app
from sqlalchemy import exc
from src.models import bcrypt
from src.common.authentication import Auth

user_api = Blueprint('user_api', __name__)
user_schema = UserSchema()

@user_api.route('/register', methods=['POST'])
def add_user():
    user = User(request.json)
    db.session.add(user)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "Error encountred", 500
    return "Successfully user registered", 200

@user_api.route('/user/<username>', methods=['GET'])
@Auth.auth_required
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "user not registered", 404
    return user_schema.jsonify(user), 200

@user_api.route('/login', methods=['GET'])
def login():
    auth = request.authorization
    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return "user not registered", 404
    if bcrypt.check_password_hash(user.password, auth.password):
        path = os.path.join("tmp", "cookies", user.username)
        if os.path.exists(path):
            with open(path, 'r') as cookie:
                c  = cookie.readlines()
                token = c[1].rstrip('\n')
                return jsonify({'message': 'user already logged in', 'token': token})
        else:
            token = Auth.generate_token(user.username)
            with open(path, "wa") as cookie:
                cookie.write(user.username+'\n')
                cookie.write(token+'\n')
            return token
    else:
        return "username or password incorrect", 404

@user_api.route('/logout', methods=['GET'])
@Auth.auth_required
def logout():
    token=None
    if "x-api-key" in request.headers:
        token = request.headers.get("x-api-key", None)
    if not token:
        return "token missing", 403
    userinfo = Auth.decode_token(token)
    username = userinfo.get('username', None)
    path = os.path.join("tmp", "cookies", username)
    try:
        os.remove(path)
    except OSError as ex:
        app.logger.error(ex)
        return 'cookie matching or remove error', 500
    return 'user logged out successfully', 200

@user_api.route('/user/<username>', methods=['PUT'])
@Auth.auth_required
def update_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "user not registered", 404
    for key, value in request.json.items():
        user.__setattr__(key, value)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "Error encountred", 500
    return user_schema.jsonify(user), 200

@user_api.route('/user/<username>', methods=['DELETE'])
@Auth.auth_required
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        return "user not registered", 404
    try:
        db.session.delete(user)
        db.session.commit()
    except exc.SQLAlchemyError as ex:
        app.logger.debug(ex)
        return "Error encountred", 500
    return "user deleted successfully", 200