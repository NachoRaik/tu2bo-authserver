from flask import Blueprint, request, jsonify
from flask import current_app as app
from database.models.user_stat import UserStat

bp_monitor = Blueprint("bp_monitor", __name__)

# -- Endpoints

@bp_monitor.route('/ping')
def ping():
    return "Authserver is up!"

@bp_monitor.route('/stats')
def stats():
    response = []
    user_stats = UserStat.objects
    for stat in user_stats:
        response.append({"num_users": stat.num_users, "timestamp": stat.timestamp})
    request_response = jsonify(response)
    request_response.status_code = 200
    return request_response
