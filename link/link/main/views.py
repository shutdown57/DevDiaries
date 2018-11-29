from flask import render_template

from main import bp_main
from link.models import Link


@bp_main.route('/', methods=['GET'])
def index():
    links = Link.query.order_by(Link.id.desc()).paginate(per_page=10)
    return render_template('index.html', links=links)


@bp_main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@bp_main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
