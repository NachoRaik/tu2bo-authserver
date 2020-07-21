from flask import Flask, request, Response
from flask_cors import CORS
from database.db import initialize_db
from config import DevelopmentConfig
from flask_swagger_ui import get_swaggerui_blueprint
import logging

# -- Server setup and config

JSON_TYPE = "application/json"

# -- App setup
def setup_blueprints(app):
    from controllers import users, monitoring
    
    app.register_blueprint(users.construct_blueprint(app))
    app.register_blueprint(monitoring.bp_monitor)

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
    CORS(app)
    app.config.from_object(config)
    app.logger.setLevel(logging.DEBUG)
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
