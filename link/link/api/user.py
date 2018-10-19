"""User views module"""

from flask import request
from flask_login import current_user

from api import bp_api
from user.validation import UserValidate
from user.models import User
from common.extensions import db
from common.utils import timestamp, response
from auth.auth import basic_auth, token_auth


prefix = '/v1/users'


# FIXME use reject first pattern
@bp_api.route(prefix + '/pages/<int:page>', methods=['GET'])
@bp_api.route(prefix + '/', methods=['GET'])
@token_auth.login_required
def get_users(page: int=None):
    if current_user.can('mod'):
        users = User.query.paginate()
        if not page:
            data = {
                'has_prev': users.has_prev,
                'has_next': users.has_next,
                'pages': users.pages,
                'users': [user.to_json() for user in users.items],
                'page': users.page,
                'total': users.total
            }
            return response(data=data)
        elif users.pages >= page:
            users.page = page
            data = {
                'has_prev': users.has_prev,
                'has_next': users.has_next,
                'pages': users.pages,
                'users': [user.to_json() for user in users.items],
                'page': users.page,
                'total': users.total
            }
            return response(data=data)
        else:
            return response(status_code=404)
    return response(status_code=403)


@bp_api.route(prefix + '/<int:id>', methods=['GET'])
@basic_auth.login_required
def get_user(id: int):
    return response(data=current_user.to_json())


@bp_api.route(prefix + '/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    if user_data and 'email' in user_data.keys() and \
            'password' in user_data.keys():
        if UserValidate.email(user_data['email']) and \
                UserValidate.password(user_data['password']):
            user = User.create(email=user_data['email'],
                               password_=user_data['password'])
            if user:
                return response(data=user.to_json(), status_code=201)
            return response(status_code=409)  # Conflict: user already exists
        else:
            return response(message='user entries validation failed',
                            status_code=400)
    return response(status_code=400)


@bp_api.route(prefix + '/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id: int):
    if (hasattr(current_user, 'id') and current_user.id == id) or \
            current_user.can('mod'):
        current_user.active = False
        current_user.token = None
        user_email = current_user.email
        db.session.add(current_user)
        db.session.commit()
        return response(status_code=202,
                        message='User {email} has been deleted'.format(
                            email=user_email))
    return response(status_code=404)


@bp_api.route(prefix + '/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id: int=None):
    data = request.get_json()
    # print(id == current_user.id)
    for key in data:
        if hasattr(current_user.info, key):
            if key == 'bio' and UserValidate.name(data['bio']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'phone_number' and \
                UserValidate.phone_number(data['phone_number']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'first_name' and UserValidate.name(data['first_name']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'last_name' and UserValidate.name(data['last_name']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'job' and UserValidate.name(data['job']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'city' and UserValidate.name(data['city']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'country' and UserValidate.name(data['country']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            elif key == 'birthday' and UserValidate.birthday(data['birthday']):
                setattr(current_user.info, key, data[key])
                db.session.add(current_user)
            else:
                return response(message='Data validation error',
                                status_code=400)

    current_user.info.updated_at = timestamp()
    db.session.commit()
    return response(data=current_user.to_json(), status_code=201)


@bp_api.route(prefix + '/token', methods=['POST'])
@basic_auth.login_required
def new_token():
    if current_user.token is None:
        current_user.generate_token()
        current_user.info.updated_at = timestamp()
        db.session.add(current_user)
        db.session.commit()
    return response(data={'token': current_user.token}, status_code=202)


@bp_api.route(prefix + '/token', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    current_user.token = None
    db.session.add(current_user)
    db.session.commit()
    return response(status_code=202,
        message='Token user {email} has been revoked'.format(
            email=current_user.email))
