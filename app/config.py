import os
from datetime import timedelta

class Config(object):
    def __init__(self):
        #self.DELAY = timedelta(milliseconds=1)
        self.DEBUG = False
        self.TESTING = False
        self.MONGODB_SETTINGS = {
	        'db': 'authserver-db',
	        'host': 'mongodb://authserver-db:27017/authserver-db'
        }
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'default')
        self.MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
        self.MAIL_PORT = os.getenv('MAIL_PORT', 465)
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'default')
        self.MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME', 'default')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'default')
        self.MAIL_USE_SSL = True
        self.RESET_CODE_TTL = timedelta(hours=1)

class ProductionConfig(Config):
    def __init__(self):
        self.DELAY = timedelta(days=1)
        super().__init__()
        self.MONGODB_SETTINGS = {
	        'host': os.getenv('MONGODB_URI'),
            'retryWrites': False
        }

class DevelopmentConfig(Config):
    def __init__(self):
        self.DELAY = timedelta(minutes=1)
        super().__init__()
        self.TESTING = True

class TestingConfig(Config):
    def __init__(self):
        self.DELAY = timedelta(milliseconds=1)
        super().__init__()
        self.TESTING = True
        self.MONGODB_SETTINGS = {
	        'db': 'authserver-db-test',
	        'host': 'mongomock://localhost',
            'connect': False,
        }
        self.RESET_CODE_TTL = timedelta(milliseconds=1)
