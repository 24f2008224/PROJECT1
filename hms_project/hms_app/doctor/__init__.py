from flask import Blueprint

doctor_bp = Blueprint('doctor', __name__)

from hms_app.doctor import routes
