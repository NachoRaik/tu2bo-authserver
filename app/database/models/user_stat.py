from database.db import db

class UserStat(db.Document):
    id = db.SequenceField(primary_key=True)
    num_users = db.IntField(required=True)
    timestamp = db.StringField(required=True)
