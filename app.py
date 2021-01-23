from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_sqlalchemy import SQLAlchemy

from security import authenticate, identity
from resources.user import UserRegister
from resources.items import ItemList, Item


app = Flask(__name__)

app.secret_key = "do_not_use_in_production"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
db.init_app(app)

api = Api(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

# Auth resource
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)


@app.before_first_request
def create_tables():
    print("Creating tables")
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
