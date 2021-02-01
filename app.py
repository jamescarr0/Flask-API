from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import UserRegister, UserLogin, User
from resources.items import ItemList, Item
from resources.store import Store, StoreList
from resources.token_refresh import TokenRefresh

app = Flask(__name__)

app.secret_key = "do_not_use_in_production"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

# API Resources / End-points.
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')


@app.before_first_request
def create_tables():
    """ Once the application is running, before the very first request create database tables. """
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
