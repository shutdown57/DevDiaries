from flask import Blueprint


bp_api = Blueprint('bp_api', __name__)

from . import user
from . import link
