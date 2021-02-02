##################################
# API Resources Endpoints / URLS #
##################################

from api import api

# API Resource objects
from api.resources.user import UserRegister, UserLogin, UserLogout, User
from api.resources.items import ItemList, Item
from api.resources.store import Store, StoreList
from api.resources.token_refresh import TokenRefresh

# API Endpoints. (Resource Class, 'URL/Endpoint/<type:variable>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')
