from flask import Blueprint

patient_bp = Blueprint('patient', __name__)

from hms_app.patient import routes
