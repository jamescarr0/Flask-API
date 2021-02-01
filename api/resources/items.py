from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_refresh_token_required,
    jwt_optional,
    get_jwt_identity,
    jwt_required
)

from api.models.itemmodel import ItemModel


class Item(Resource):

    @jwt_required
    # Any token required, Fresh true or false.
    def get(self, name):
        # Return requested item
        item = ItemModel.find_by_name(name)
        return (item.json(), 200) if item else ({'message': 'item not found'}, 404)

    @jwt_refresh_token_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item exists'}, 400
        data = request.get_json()
        if 'price' and 'store_id' not in data:
            return {'message': 'Items require price and store id'}

        new_item = ItemModel(name, data['price'], data['store_id'])
        try:
            new_item.save_to_db()
        except:
            return {"message": "An error occurred"}, 500  # Internal server error (not users fault)
        return new_item.json(), 201

    @jwt_refresh_token_required
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    @jwt_refresh_token_required
    def put(self, name):
        data = request.get_json()
        item = ItemModel.find_by_name(name)
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price'], data['store_id']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @jwt_optional
    # EXAMPLE of using jwt_optional decorator. - Partially Protect The Endpoint.
    # If no JWT is sent with request, get_jet_identity() will return None.
    # Invalid JWT's including those expired will return an error.
    def get(self):
        # Logged in users will have a JWT token containing user id.
        # If logged in return all items.
        if get_jwt_identity() is not None:  # UserModel.find_by_userid(get_jwt_identity()):
            return [item.json() for item in ItemModel.find_all()], 200

        # User not logged in.  Return item names only and message prompting more data available when logged in.
        return {
                   "items": [item.name for item in ItemModel.find_all()],
                   "message": "Login for more data"
               }, 200
