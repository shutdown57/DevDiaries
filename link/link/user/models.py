"""User models module"""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from binascii import hexlify
from flask import url_for
from os import urandom
import uuid

from common.extensions import db
from common.utils import timestamp


class User(db.Model, UserMixin):
    """
    User model
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    token = db.Column(db.String(64))
    active = db.Column(db.Boolean, server_default='1')

    # Relationships
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    info_id = db.Column(db.Integer, db.ForeignKey('info.id'))
    info = db.relationship('Info', backref=db.backref('user', uselist=False))

    links = db.relationship('Link', backref='user', lazy='dynamic')

    def get_id(self):
        """
        Get token to load user
        """
        return self.token

    def is_active(self):
        """
        To find user is active or not
        """
        return True

    def is_anonymous(self):
        """
        The logged in user is not anonymous any more
        """
        return False

    def is_authenticated(self):
        """
        User logged in
        """
        return True

    @property
    def password(self):
        """
        Raise an error if call password property
        """
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password_: str) -> None:
        """
        Generate hashed password
        """
        self.password_hash = generate_password_hash(password_)
        self.token = None

    def verify_password(self, password_: str) -> bool:
        """
        Verify user password with given password
        """
        return check_password_hash(self.password_hash, password_)

    @classmethod
    def create(cls, email: str, password_: str):
        """
        Create if user does not exist
        :param email: user object as string
        :param password_: user password as string
        """
        old_user = User.query.filter_by(email=email).first() \
            if User.query.filter_by(email=email).first() else None
        if old_user and old_user.active:
            return False
        elif old_user and not old_user.active:
            old_user.active = True
            db.session.add(old_user)
            db.session.commit()
            return old_user
        else:
            user = cls(email=email)
            user.password = password_
            user.generate_token()

            user.role = Role.query.filter_by(name='user').first()
            user.info = Info()

            db.session.add(user)
            db.session.commit()
            return user

    def generate_token(self) -> str:
        """
        Generate user token
        """
        self.token = hexlify(urandom(32)).decode('utf-8')
        return self.token

    def generate_api_key(self) -> str:
        """
        Generate an API key
        """
        self.info.api_key = uuid.uuid4().hex
        return self.info.api_key

    def to_json(self) -> dict:
        """
        Convert user data to dict object
        """
        return {
            'email': self.email,
            'token': self.token,
            'role_name': self.role.name,
            'info': self.info.to_json(),
            '_links': {
                'token': url_for('bp_user.new_token', _external=True),
                'user': url_for('bp_user.get_user', id=self.id, _external=True)
            }
        }

    def can(self, user_type: str) -> bool:
        """
        user previlage if return true user has permission
        else user has not permission
        :param user_type: user type
        :return bool: Convert user permission to bool object
        """
        return (int(self.role.permission, 16) & \
                int(Permission.TYPES[user_type], 16)) \
                == int(Permission.TYPES[user_type], 16)

    def is_admin(self) -> bool:
        """
        If user is admin return true else return false
        """
        return self.can('admin')

    def __repr__(self) -> str:
        """
        Stringify user object to print in console
        """
        return '<USER ID={id} EMAIL={email} TOKEN={token}>'.format(
            id=self.id, email=self.email, token=True if self.token else False)


class Info(db.Model):
    """
    User information model
    """
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(20), nullable=True)
    last_name = db.Column(db.String(30), nullable=True)
    birthday = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.Text, nullable=True)
    country = db.Column(db.String(20), nullable=True)
    city = db.Column(db.String(20), nullable=True)
    phone_number = db.Column(db.String(15), nullable=True)
    job = db.Column(db.String(50), nullable=True)

    api_key = db.Column(db.String(256), nullable=True)

    created_at = db.Column(db.Integer, default=timestamp)
    updated_at = db.Column(db.Integer, default=timestamp, onupdate=timestamp)
    last_seen_at = db.Column(db.Integer, default=timestamp)

    def to_json(self) -> dict:
        """
        Convert user info object to dict object
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birthday': self.birthday,
            'bio': self.bio,
            'country': self.country,
            'city': self.city,
            'phone_number': self.phone_number,
            'job': self.job,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'last_seen': self.last_seen_at,
            'api_key': self.api_key or 'If you were moderator!'
        }

    def __repr__(self) -> str:
        """
        Stringify info object to print in console
        """
        return '<INFO ID={id} NAME={first_name} UPDATED_AT={updated_at}>'.format(
            id=self.id, first_name=self.first_name, updated_at=self.updated_at
        )


class Permission:
    """
    user previlage class
    """
    GUEST = 0x01
    USER = 0x02
    MOD = 0x04
    ADMIN = 0x80
    TYPES = {
        'guest': 0x01,
        'user': 0x02,
        'mod': 0x04,
        'admin': 0x80
    }


class Role(db.Model):
    """
    User role model
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(15), default='user')
    permission = db.Column(db.Integer, default=Permission.USER)

    users = db.relationship('User', backref='role', lazy='dynamic')

    @classmethod
    def init_roles(cls) -> None:
        """
        add user roles to role table
        """
        guest = cls(name='guest', permission=Permission.GUEST)
        user = cls(name='user', permission=Permission.USER)
        mod = cls(name='mod', permission=Permission.MOD)
        admin = cls(name='admin', permission=Permission.ADMIN)

        db.session.add_all([guest, user, mod, admin])
        db.session.commit()

    def __repr__(self) -> str:
        """
        Stringify role object to print in console
        """
        return '<ROLE ID={id} NAME={name} PERMISSION={permission}>'.format(
            id=self.id, name=self.name, permission=self.permission)


class Anonymous(AnonymousUserMixin):
    """
    Handle anonymous users
    """
    def __init__(self) -> None:
        self.email = 'guest'

    def can(self, user_type: str) -> bool:
        return False

    def is_admin(self) -> bool:
        return False

    def is_authenticated(self) -> bool:
        return False
