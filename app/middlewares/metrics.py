from flask import current_app as app
from functools import wraps
from database.models.user import User
from database.models.user_stat import UserStat
from datetime import datetime

TIME_FORMAT = "%m/%d/%y %H:%M:%S"

def should_be_saved():
    is_time = True
    if len(UserStat.objects) != 0:
        last_record_timestamp = UserStat.objects.order_by('-id').first().timestamp
        last_record_to_datetime = datetime.strptime(last_record_timestamp, TIME_FORMAT)
        is_time = (datetime.now() - last_record_to_datetime) > app.config['DELAY']
    return is_time

def add_user_count(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        response = f(*args, **kwargs)
        if response.status_code == 200 and should_be_saved(): 
            num_users = len(User.objects)
            timestamp = datetime.now().strftime(TIME_FORMAT)
            user_stat = UserStat(num_users=num_users, timestamp=timestamp)
            user_stat.save()
        return response
    return decorated