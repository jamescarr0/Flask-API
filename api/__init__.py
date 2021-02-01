from flask import Flask
from flask import Blueprint

from api.db import db
from api.auth import jwt
from api.auth.errors import jwt_callbacks  # Custom JWT error responses.
from api.config import Config  # Import application configuration variables.
from api.resources import api  # Import the API resource endpoints.


def create_app():
    # Initialise the flask application
    app = Flask(__name__)

    # Load flask configuration variables from Config object.
    app.config.from_object(Config)

    # Initialise extension objects.
    db.init_app(app)
    api_blueprint = Blueprint('api', __name__)
    api.init_app(api_blueprint)
    jwt.init_app(app)

    # Register the API blueprint.
    app.register_blueprint(api_blueprint, url_prefix=Config.API_URL_PREFIX)

    @app.before_first_request
    def create_tables():
        """ Once the application is running, before the very first request create database tables. """
        db.create_all()

    return app
