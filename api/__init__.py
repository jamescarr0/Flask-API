from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask import Blueprint

from api.db import db
from api.config import Config

api = Api()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    api_blueprint = Blueprint('api', __name__)
    api.init_app(api_blueprint)
    jwt.init_app(app)

    from api.resources.user import UserRegister, UserLogin, User
    from api.resources.items import ItemList, Item
    from api.resources.store import Store, StoreList
    from api.resources.token_refresh import TokenRefresh

    api.add_resource(Store, '/store/<string:name>')
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(ItemList, '/items')
    api.add_resource(UserRegister, '/register')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TokenRefresh, '/refresh')

    app.register_blueprint(api_blueprint, url_prefix=Config.API_URL_PREFIX)

    @app.before_first_request
    def create_tables():
        """ Once the application is running, before the very first request create database tables. """
        db.create_all()

    return app
