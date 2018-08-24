from flask import render_template

from app.main import bp_main


@bp_main.route('/', methods=['GET'])
def index():
    return render_template('index.html')
