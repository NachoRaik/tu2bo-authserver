import os
basedir = os.path.abspath(os.path.dirname(__file__))


firebaseConfig = {
    "apiKey": "AIzaSyCD9EB8Kaos1qqSuS0isNv1BPz9ba48PwY",
    "authDomain": "tu2bo-131ec.firebaseapp.com",
    "databaseURL": "https://tu2bo-131ec.firebaseio.com",
    "projectId": "tu2bo-131ec",
    "storageBucket": "tu2bo-131ec.appspot.com",
    "messagingSenderId": "665671721983",
    "appId": "1:665671721983:web:a2a2cfa1cee89044ed3dca",
    "measurementId": "G-VXN8NZ6J2X"
  }


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
