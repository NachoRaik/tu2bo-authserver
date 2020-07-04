import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
	    'db': 'authserver-db',
	    'host': 'mongodb://authserver-db:27017/authserver-db'
    }
    SECRET_KEY = os.getenv('SECRET_KEY', 'default')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 465)
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default')
    MAIL_PASSWORD = os.getenv('MAIL_USERNAME', 'default')
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    MONGODB_SETTINGS = {
	    'host': os.getenv('MONGODB_URI'),
        'retryWrites': False
    }

class DevelopmentConfig(Config):
    TESTING = True

class TestingConfig(Config, object):
    TESTING = True
    MONGODB_SETTINGS = {
	    'db': 'authserver-db-test',
	    'host': 'mongomock://localhost',
        'connect': False,
    }