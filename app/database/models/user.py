from database.db import db

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    email = db.StringField(required=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    last_name = db.StringField(required=True)

    def serialize(self): #to select what fields to return in get
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'last_name': self.last_name
        }
