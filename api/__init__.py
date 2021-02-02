from flask import Flask
from flask import Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from api.auth.errors import jwt_callbacks  # Custom JWT error responses.
from api.config import Config  # Import application configuration variables.
from api.auth import jwt

db = SQLAlchemy()
api = Api()


def create_app():
    # Initialise the flask application
    app = Flask(__name__)

    # Load flask configuration variables from Config object.
    app.config.from_object(Config)

    # Initialise extension objects.
    db.init_app(app)
    jwt.init_app(app)

    api_blueprint = Blueprint('api', __name__)
    api.init_app(api_blueprint)

    # Import resource endpoints / URLS and register API blueprint.
    from api import urls
    app.register_blueprint(api_blueprint, url_prefix=Config.API_URL_PREFIX)

    @app.before_first_request
    def create_tables():
        """ Once the application is running, before the very first request create database tables. """
        db.create_all()

    return app
