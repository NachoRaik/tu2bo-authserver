import os

class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.MONGODB_SETTINGS = {
	        'db': 'authserver-db',
	        'host': 'mongodb://authserver-db:27017/authserver-db'
        }
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'default')

class ProductionConfig(Config):
    def __init__(self):
        super().__init__()
        self.MONGODB_SETTINGS = {
	        'host': os.getenv('MONGODB_URI'),
            'retryWrites': False
        }

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.TESTING = True

class TestingConfig(Config):
    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.MONGODB_SETTINGS = {
	        'db': 'authserver-db-test',
	        'host': 'mongomock://localhost',
            'connect': False,
        }
