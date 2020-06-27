from flask import Blueprint, request, jsonify
from flask import current_app as app
from database.models.user import User

bp_monitor = Blueprint("bp_monitor", __name__)

# -- Endpoints

@bp_monitor.route('/ping')
def ping():
    return "Authserver is up!"

@bp_monitor.route('/stats')
def stats():
    num_users = User.objects.count()
    response = jsonify({"num_users": num_users})
    response.status_code = 200
    return response

