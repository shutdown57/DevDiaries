from flask import Flask, render_template

from config import configs
from common.moment import Moment
from common.extensions import login_manager
from common.utils import SessionInterface
from user.models import Anonymous, User
from link.models import Link


def create_app(config_name='default'):
    """
    Create application inctanse by given configs
    :param config_name str: The config name to create app inctanse
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(configs[config_name])
    app.jinja_env.globals['Moment'] = Moment

    # Initializing
    #  db.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'bp_auth.login_create'
    login_manager.anonymous_user = Anonymous

    app.session_interface = SessionInterface()

    @login_manager.user_loader
    def load_user(token: str) -> User:
        """
        Handler for login manager to load user by token
        :param token str: Unique user token
        :return: User if find by token else Anonymous
        """
        user = User.query.filter_by(token=token).first()
        if user:
            return user
        return Anonymous()

    from user import bp_user
    from link import bp_link
    from auth import bp_auth
    from main import bp_main
    from api import bp_api

    app.register_blueprint(bp_main)
    app.register_blueprint(bp_auth, url_prefix='/auth')
    app.register_blueprint(bp_user, url_prefix='/users')
    app.register_blueprint(bp_link, url_prefix='/links')
    app.register_blueprint(bp_api, url_prefix='/api')

    return app
