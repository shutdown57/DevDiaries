from flask import Blueprint


bp_link = Blueprint('bp_link', __name__)

from . import views
