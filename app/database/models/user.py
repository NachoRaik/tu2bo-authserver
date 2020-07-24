from database.db import db

class User(db.Document):
    id = db.SequenceField(primary_key=True)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=False)
    username = db.StringField(required=True, unique=True)
    profile_pic = db.StringField(required=False)
    is_blocked = db.BooleanField(required=False, default=False)
    provider = db.StringField(required=True)

    def serialize(self): #to select what fields to return in get
        profile_info = {}
        if self.profile_pic:
            profile_info['picture'] = self.profile_pic

        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'profile': profile_info
        }

    def serialize_admin(self):
        fields = self.serialize()
        fields['is_blocked'] = self.is_blocked
        return fields
