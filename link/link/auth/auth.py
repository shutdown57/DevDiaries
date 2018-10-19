"""Authorization users module"""

from flask_login import login_user
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from user.models import User
from common.utils import response
from common.extensions import db


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth('Bearer')
token_optional_auth = HTTPTokenAuth('Bearer')


@basic_auth.verify_password
def verify_password(email: str, password: str) -> bool:
    """
    Handle basic auth user request
    :param email: <str> user email
    :param password: <str> user password
    :return: <bool> return true if user exists and actived else return false
    """
    if not email or not password:
        return False
    user = User.query.filter_by(email=email).first()
    if user is None or not user.verify_password(password):
        return False
    if not user.active:
        return False
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return True


@basic_auth.error_handler
def password_error() -> tuple:
    """
    Basic auth error handling
    :return: <tuple> with status code 401, headers authentication required and
    data authentication required
    """
    response_ = {'error': 'authentication required'}
    headers = {'WWW-Authenticate': 'Bearer realm=authentication Required'}
    return response(data=response_, status_code=401, headers=headers)


@token_auth.verify_token
def verify_token(token: str) -> bool:
    """
    Handle bearer auth token
    :param token: <str> user token
    :return: <bool> return true if user exists and has a valid token else false
    """
    user = User.query.filter_by(token=token).first()
    if user is None:
        return False
    if not user.active:
        return False
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return True


@token_auth.error_handler
def token_error() -> tuple:
    """
    Bearer auth error handling
    :return: <tuple> with status code 401, headers authentication required and
    data authentication required
    """
    response_ = {'error': 'authentication required'}
    headers = {'WWW-Authenticate': 'Bearer realm="Authentication Required"'}
    return response(data=response_, status_code=401, headers=headers)


@token_optional_auth.verify_token
def verify_optional_token(token: str) -> bool:
    """
    Handle optional bearer token
    :param token: <str> user token or empty string
    :return: <bool> if user sent a token it will use verify_token function
    with token parameter (to authenticate user token) if user sent none token
    it will return true
    """
    if token == '':
        return True
    return verify_token(token)
