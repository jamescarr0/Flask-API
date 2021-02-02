from __future__ import annotations
from api import db


class StoreModel(db.Model):
    # Create store table define the columns.
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Lazy enabled.  Call .all() to access the items.
    # Stops the database being access and returning a list of items when a
    # StoreModel is created.  Costs less (saves resources).
    items = db.relationship('ItemModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, name):
        """ Store object constructor. """
        self.name = name

    def json(self) -> dict:
        # Lazy dynamic enabled, when this method is called, the database is accessed and a list of items
        # is returned.  This results in a slower return of items, but faster creation of Store.
        # Returns store details in JSON format.  flaskRESTFUL converts dict -> JSON.
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items]
        }

    def save_to_db(self):
        """ Save Store object to the database. """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """ Delete the store object from the database. """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name) -> StoreModel:
        """ Retrieve a single store by name from the database. """
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> list[StoreModel]:
        """ Retrieve all Store objects from the database. """
        return cls.query.all()
