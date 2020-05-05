from flask import Flask, request, jsonify
from database.db import initialize_db
from config import firebaseConfig
from config import DevelopmentConfig
import pyrebase
import os



def create_authserver(config= DevelopmentConfig()):
    # ------- initial server configuration
    app = Flask(__name__)

    # ------- postgres
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = initialize_db(app)

    import users, authentication

    app.register_blueprint(users.bp_users)
    app.register_blueprint(authentication.bp_auth)

    # main endpoints

    @app.route("/")
    def hello():
        return "This is de auth server"


    @app.route("/ping")
    def ping():
        return "Auth server is alive"

    return app

app = create_authserver()


if __name__ == '__main__':
    app.run()
