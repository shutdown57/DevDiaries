from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from common.extensions import db
from user.models import User
from admin import bp_admin


@bp_admin.route('/', methods=['GET'])
@login_required
def index():
    admin = User.query.filter_by(id=1).first()
    return render_template('admin/index.html', admin=admin)
