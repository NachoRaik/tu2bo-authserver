from flask import Flask, request, Response
from database.db import initialize_db
from config import DevelopmentConfig
from flask_swagger_ui import get_swaggerui_blueprint

# -- Server setup and config

JSON_TYPE = "application/json"

# -- App setup
def setup_blueprints(app):
    from controllers import users, monitoring, auth_users

    app.register_blueprint(users.bp_users)
    app.register_blueprint(monitoring.bp_monitor)
    app.register_blueprint(auth_users.bp_auth_users)

def setup_swaggerui(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Auth Server"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)



# -- App creation

def create_app(config=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config)
    db = initialize_db(app)

    setup_blueprints(app)
    setup_swaggerui(app)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    # -- Unassigned endpoints
    @app.route('/')
    def hello():
        return "This is the Auth Server!"

    return app
