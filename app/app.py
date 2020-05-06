from flask import Flask, request, Response
from database.db import initialize_db
from config import DevelopmentConfig

# -- Server setup and config

JSON_TYPE = "application/json"

# -- App creation

def create_app(config=DevelopmentConfig()):
    app = Flask(__name__)
    app.config.from_object(config)
    db = initialize_db(app)

    import controllers.users as users, controllers.monitoring as monitoring

    app.register_blueprint(users.bp_users)
    app.register_blueprint(monitoring.bp_monitor)
    
    # -- Unassigned endpoints
    @app.route('/')
    def hello():
        return "This is the Auth Server!"

    @app.route('/login', methods=['POST'])
    def register():
        return "TODO: login"

    return app


app = create_app()

# -- Run

if __name__ == '__main__':
    app.run(host="localhost", port="5000")