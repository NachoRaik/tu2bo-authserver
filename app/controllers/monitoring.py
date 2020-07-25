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
    default_initial_date = (datetime.now() - timedelta(days=1)).strftime(TIME_FORMAT)
    initial_date = request.args.get('initial_date') if 'initial_date' in request.args else default_initial_date 
    initial_date_to_timestamp = datetime.strptime(initial_date, TIME_FORMAT)
    
    default_final_date = (datetime.now()).strftime(TIME_FORMAT)
    final_date = request.args.get('final_date') if 'final_date' in request.args else default_final_date    
    final_date_to_timestamp = datetime.strptime(final_date, TIME_FORMAT)

    response = []
    user_stats = UserStat.objects

    for stat in user_stats:
        act_timestamp = datetime.strptime(stat.timestamp, TIME_FORMAT)
        if initial_date_to_timestamp <= act_timestamp and act_timestamp <= final_date_to_timestamp: 
            response.append({"count": stat.num_users, "date": stat.timestamp})
   
    request_response = jsonify(response)
    request_response.status_code = 200
    return request_response
