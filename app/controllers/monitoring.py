from flask import Blueprint, request, jsonify
from flask import current_app as app
from database.models.user import User

bp_monitor = Blueprint("bp_monitor", __name__)

# -- Endpoints

@bp_monitor.route('/ping')
def ping():
    return "Authserver is up!"


