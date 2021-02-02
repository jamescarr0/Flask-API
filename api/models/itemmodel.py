from __future__ import annotations
from api import db


class ItemModel(db.Model):
    # Create items table and define the columns
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.FLOAT(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        """ Item object constructor """
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> dict:
        """
        Returns Item details in JSON format
        flaskRESTUL converts python dict to JSON.
        """
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'store_id': self.store_id
        }

    def save_to_db(self):
        """ Save the Item object to the database """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ Delete Item object from database """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> ItemModel:
        """
        Retrieve a single Item object by name from the database.
        Returns:
            Item object
        """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> list[ItemModel]:
        """ Retrieve all Item objects from the database. """
        return cls.query.all()
