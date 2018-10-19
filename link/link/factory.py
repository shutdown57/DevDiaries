from flask import Flask, render_template

from config import configs
from common.extensions import login_manager
from common.utils import SessionInterface
from user.models import Anonymous, User


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    # Initializing
    login_manager.session_protection = 'strong'
    login_manager.anonymous_user = Anonymous

    app.session_interface = SessionInterface()

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @login_manager.user_loader
    def load_user(token: str) -> User:
        return User.query.filter_by(token=token).first()

    from user import bp_user
    from link import bp_link
    from auth import bp_auth
    from api import bp_api

    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_user, url_prefix='/users')
    app.register_blueprint(bp_link, url_prefix='/links')
    app.register_blueprint(bp_api, url_prefix='/api')

    return app
