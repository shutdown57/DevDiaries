from flask import Flask, render_template

from config import configs


def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(configs[config_name])

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    return app
