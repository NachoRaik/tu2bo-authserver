from database.db import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())

    def __init__(self, username, first_name, last_name):
        self.name = username
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return '<id {} username {} >'.format(self.id,self.username  )

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name':self.last_name
        }
