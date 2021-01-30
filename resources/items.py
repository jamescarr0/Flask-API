from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from models.itemmodel import ItemModel


class Item(Resource):

    def get(self, name):
        item = ItemModel.find_by_name(name)
        return (item.json(), 200) if item else ({'message': 'item not found'}, 404)

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

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

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
    @jwt_required
    def get(self):
        return {"Items": [item.json() for item in ItemModel.find_all()]}, 200
