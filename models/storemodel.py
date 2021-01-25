from db import db


class StoreModel(db.Model):

    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Lazy enabled.  Call .all() to access the items.
    # Stops the database being access and returning a list of items when a
    # StoreModel is created.  Costs less (saves resources).
    items = db.relationship('ItemModel', lazy='dynamic', cascade="all, delete")

    def __init__(self, name):
        self.name = name

    def json(self):
        # Lazy dynamic enabled, when this method is called, the database is accessed and a list of items
        # is returned.  This results in a slower return of items, but faster creation of Store.
        return {'name': self.name, 'items': [item.json() for item in self.items]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
