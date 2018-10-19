import os


base_uri = os.path.abspath(os.path.dirname(__file__))
default_secret_key = os.urandom(24)


class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', default_secret_key)
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_uri, 'db-dev.sqlite')


class ProductConfig(Config):
    DEBUG = False
    TESTING = False
    PREFERRED_URL_SCHEME = 'https'
    # TODO Configuration MariaDB for Production


class TestConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_uri, 'db-test.sqlite')


configs = {
    'development': DevelopConfig,
    'product': ProductConfig,
    'test': TestConfig,
    'default': DevelopConfig
}
