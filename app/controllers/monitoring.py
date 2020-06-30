from flask import Blueprint, request, jsonify
from flask import current_app as app
from database.models.user_stat import UserStat
from datetime import datetime

bp_monitor = Blueprint("bp_monitor", __name__)

TIME_FORMAT = "%m/%d/%y %H:%M:%S"

# -- Endpoints

@bp_monitor.route('/ping')
def ping():
    return "Authserver is up!"

@bp_monitor.route('/stats')
def stats():
    date = request.args.get('timestamp')
    date_to_timestamp = datetime.strptime(date, TIME_FORMAT)
    response = []
    user_stats = UserStat.objects
    for stat in user_stats:
        act_timestamp = datetime.strptime(stat.timestamp, TIME_FORMAT)
        if date_to_timestamp < act_timestamp: 
            response.append({"num_users": stat.num_users, "timestamp": stat.timestamp})
    request_response = jsonify(response)
    request_response.status_code = 200
    return request_response
