from database.db import db
import datetime as dt

class ResetPasswordCode(db.Document):
    code = db.IntField()
    user_mail = db.StringField()
    expire_at = db.DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['expire_at'], 'expireAfterSeconds': 0} # ttl
        ]
    }