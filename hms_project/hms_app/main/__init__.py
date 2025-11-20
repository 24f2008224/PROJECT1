from flask import Blueprint

main = Blueprint('main', __name__)

from hms_app.main import routes
