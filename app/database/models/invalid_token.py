from database.db import db
import datetime as dt

class InvalidToken(db.Document): # blacklist
    token = db.StringField(unique=True)
    expire_at = db.DateTimeField()
    meta = {
        'indexes': [
            {'fields': ['expire_at'], 'expireAfterSeconds': 0} # ttl
        ]
    }