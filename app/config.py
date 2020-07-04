import os

class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
	    'db': 'authserver-db',
	    'host': 'mongodb://authserver-db:27017/authserver-db'
    }
    SECRET_KEY = os.getenv('SECRET_KEY', 'default')

class ProductionConfig(Config):
    MONGODB_SETTINGS = {
	    'host': os.getenv('MONGODB_URI'),
        'retryWrites': False
    }

class DevelopmentConfig(Config):
    #TESTING = True
    #DEBUG = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 456
    MAIL_USERNAME = 'olifer97@gmail.com'
    MAIL_PASSWORD = 'xwkzrkrufbdvsvav'
    MAIL_USE_SSL = True

class TestingConfig(Config, object):
    TESTING = True
    MONGODB_SETTINGS = {
	    'db': 'authserver-db-test',
	    'host': 'mongomock://localhost',
        'connect': False,
    }