"""User views module"""

from flask import request, render_template
from flask_login import current_user, login_required

from user import bp_user
#  from user.validation import UserValidate
#  from user.models import User
#  from common.extensions import db
#  from common.utils import timestamp, response
#  from auth.auth import basic_auth, token_auth


@bp_user.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/user', user=current_user)
