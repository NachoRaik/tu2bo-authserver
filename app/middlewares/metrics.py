from flask import Blueprint, Response, request, jsonify, make_response
from flask import current_app as app
from functools import wraps
from database.models.user import User
from database.models.user_stat import UserStat
from datetime import datetime

def add_user_count(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 200: 
            num_users = User.objects.count()
            timestamp = datetime.now().strftime("%m/%d/%y %H:%M:%S")
            user_stat = UserStat(num_users=num_users, timestamp=timestamp)
            user_stat.save()
        return response
    return decorated