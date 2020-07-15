from flask import Blueprint, request, jsonify
from flask import current_app as app
from database.models.user_stat import UserStat
from datetime import datetime, timedelta

bp_monitor = Blueprint("bp_monitor", __name__)

TIME_FORMAT = "%m/%d/%y %H:%M:%S"

# -- Endpoints

@bp_monitor.route('/ping')
def ping():
    return "Authserver is up!"

@bp_monitor.route('/stats')
def stats():
    default_date = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
    date = request.args.get('date') if 'date' in request.args else default_date
    date_to_timestamp = datetime.strptime(date, TIME_FORMAT)
    response = []
    user_stats = UserStat.objects
    for stat in user_stats:
        act_timestamp = datetime.strptime(stat.timestamp, TIME_FORMAT)
        if date_to_timestamp < act_timestamp: 
            response.append({"count": stat.num_users, "date": stat.timestamp})
    request_response = jsonify(response)
    request_response.status_code = 200
    return request_response
