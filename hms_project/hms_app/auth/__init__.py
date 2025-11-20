from flask import Blueprint

auth = Blueprint('auth', __name__)

from hms_app.auth import routes
