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
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    TESTING = True

class TestingConfig(object):
    DEBUG = False
    TESTING = True
    MONGODB_SETTINGS = {
	    'db': 'authserver-db-test',
	    'host': 'mongomock://localhost'
    }
    #MONGODB_CONNECT = False
    SECRET_KEY = '7bzRBYbgqzFWe4Y7oz6zFUIt6jE3ZOlq'
