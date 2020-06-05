import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
	    'db': 'authserver-db',
	    'host': 'mongodb://authserver-db:27017/authserver-db'
    }
    SECRET_KEY = ''

class ProductionConfig(Config):
    MONGODB_SETTINGS = {
	    'host': os.getenv('MONGODB_URI'),
        'retryWrites': False
    }
    SECRET_KEY = str(os.getenv('SECRET_KEY'))

class DevelopmentConfig(Config):
    TESTING = True

class TestingConfig(Config, object):
    TESTING = True
    MONGODB_SETTINGS = {
	    'db': 'authserver-db-test',
	    'host': 'mongomock://localhost',
        'connect': False,
    }
