import jwt
import os
import datetime
from flask import current_app as app
from functools import wraps
from flask import request
from src.models.user_model import User

class Auth:

    @staticmethod
    def generate_token(username):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': username
            }
            return jwt.encode(payload, app.config.get('SECRET_KEY', None),'HS256').decode("utf-8")
        except Exception as ex:
            app.logger.error(ex)
            return "token generating error", 404

    @staticmethod
    def decode_token(token):
        app.logger.debug(token)
        try:
            payload = jwt.decode(token, app.config.get('SECRET_KEY', None), 'HS256')
            result = {'username': payload['sub']}
            return result
        except jwt.ExpiredSignatureError as ex:
            app.logger.error(ex)
            result = {'message': 'token expired, please login again'}
            return result
        except jwt.InvalidTokenError as ex:
            app.logger.error(ex)
            result = {'message': 'invalid token, please try again with a new token'}
            return result

    @staticmethod
    def auth_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if "x-api-key" in request.headers:
                token = request.headers.get("x-api-key", None)
            if not token:
                return "token missing", 403
            userinfo = Auth.decode_token(token)
            user = User.query.filter_by(username=userinfo.get('username')).first()
            if not user:
                return 'access denied', 404
            path = os.path.join("tmp", "cookies", userinfo.get('username', None))
            if not os.path.exists(path):
                return 'access denied', 404
            return f(*args, **kwargs)
        return decorated
