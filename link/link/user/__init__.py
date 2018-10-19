from flask import Blueprint


bp_user = Blueprint('bp_user', __name__)

from . import views
