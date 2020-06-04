import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
	    'db': 'authserver-db',
	    'host': 'mongodb://authserver-db:27017/authserver-db'
    }
    SECRET_KEY = '7bzRBYbgqzFWe4Y7oz6zFUIt6jE3ZOlq'

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
