#########################################
# API Resource configuration            #
#                                       #
# Add API Resources & Endpoints Here    #
#########################################

# API framework.
from flask_restful import Api

# API Resource objects
from api.resources.user import UserRegister, UserLogin, User
from api.resources.items import ItemList, Item
from api.resources.store import Store, StoreList
from api.resources.token_refresh import TokenRefresh

api = Api()

# API Endpoints. (Resource Class, 'URL/Endpoint/<string:variables>'
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TokenRefresh, '/refresh')
