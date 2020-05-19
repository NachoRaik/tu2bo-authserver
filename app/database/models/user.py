from database.db import db

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    username = db.StringField(required=True, unique=True)

    def serialize(self): #to select what fields to return in get
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username
        }
