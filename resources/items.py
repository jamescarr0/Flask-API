from flask import request
from flask_restful import Resource
from flask_jwt import jwt_required

from models.itemmodel import ItemModel


class Item(Resource):

    def get(self, name):
        item = ItemModel.find_by_name(name)
        return (item.json(), 200) if item else ({'message': 'item not found'}, 404)

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'item exists'}, 400
        data = request.get_json()
        new_item = ItemModel(name, data['price'])
        try:
            new_item.save_to_db()
        except Exception as err:
            print(err)
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
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {"Items": [item.json() for item in ItemModel.query.all()]}, 200
