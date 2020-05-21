from flask import Flask, request, Response
from database.db import initialize_db
from config import DevelopmentConfig

# -- Server setup and config

JSON_TYPE = "application/json"

# -- App setup
def setup_blueprints(app):
    from controllers import users, monitoring, auth_users

    app.register_blueprint(users.bp_users)
    app.register_blueprint(monitoring.bp_monitor)
    app.register_blueprint(auth_users.bp_auth_users)



# -- App creation

def create_app(config=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config)
    db = initialize_db(app)

    setup_blueprints(app)

    # -- Unassigned endpoints
    @app.route('/')
    def hello():
        return "This is the Auth Server!"

    @app.route('/login', methods=['POST'])
    def register():
        return "TODO: login"

    return app



