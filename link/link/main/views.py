from flask import render_template, request

from main import bp_main
from link.models import Link


@bp_main.route('/', methods=['GET'])
def index():
    #  page = request.args.get('page', 1, type=int)
    page = 1
    links = Link.query.order_by(Link.created_at.desc()).paginate(page, per_page=10, error_out=False)
    return render_template('index.html', links=links)


@bp_main.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


@bp_main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')
