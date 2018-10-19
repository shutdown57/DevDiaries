"""Application utils modules"""

import time
from functools import wraps
from flask import g, jsonify, url_for
from flask_login import current_user
from flask.sessions import SecureCookieSessionInterface

# from src.user.models import Permission


def timestamp() -> int:
    """
    Return the current timestamp as an integer
    :return: <int> timestamp
    """
    return int(time.time())


class SessionInterface(SecureCookieSessionInterface):

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(SessionInterface, self).save_session(*args, **kwargs)


def response(message: str='', data: dict={}, status_code: int=200, headers: dict={}) -> tuple:
    """
    Handle json response to cleaner code style
    :param message: <str> if need sent specific messege
    :param data: <dict> the data to sent client
    :param status_code: <int> status code of response
    :param headers: <dict> extra headers handling
    :return: <JSON> return jsonified response
    """
    if message:
        data['message'] = message
        if headers:
            return jsonify(data), status_code, headers
        return jsonify(data), status_code
    if data:
        if headers:
            return jsonify(data), status_code, headers
        return jsonify(data), status_code
    if 399 < status_code < 500:
        status = 'failed'
        if status_code == 400:
            message = 'Bad Request'
        elif status_code == 401:
            message = 'Unauthorized'
        elif status_code == 402:
            message = 'Payment Required'
        elif status_code == 403:
            message = 'Forbidden'
        elif status_code == 404:
            message = 'Not Found'
        elif status_code == 406:
            message = 'Not Acceptable'
        elif status_code == 409:
            message = 'Conflict'
        elif status_code == 410:
            message = 'Gone'
        else:
            status_code = 400
            message = 'Bad Request'
        if headers:
            return jsonify(status=status, message=message), status_code, headers
        return jsonify(status=status, message=message), status_code
    else:
        return jsonify(data), status_code, headers


# TODO make it work
def has_permission(func, role: str, user_role: str):
    @wraps
    def decorated_func(*args, **kwargs):
        if role == user_role:
            pass
    pass
