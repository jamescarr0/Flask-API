from __future__ import annotations
from argon2 import PasswordHasher

from api import db


class UserModel(db.Model):
    # Create users table and define columns.
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # Create password hashing object. No params passed will use Argon2 Default values.
    ph = PasswordHasher()

    def __init__(self, username, password):
        """ User constructor. """
        self.username = username
        self.password = self.ph.hash(password)

    def __repr__(self) -> str:
        """ REPR - Customise console object output """
        return f"<User: _id: {self.id}, username: {self.username}>"

    def json(self) -> dict:
        """ Return User JSON.  RESTFUL Frameworks converts dict to JSON. """
        return {
            'id': self.id,
            'username': self.username
        }

    def save_to_db(self):
        """ Save User object to the database. """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete the user object from the database. """
        db.session.delete(self)
        db.session.commit()

    def verify_password(self, password) -> bool:
        """
        Verify user password against the stored password hash
        Returns:
            Bool
        """
        try:
            return self.ph.verify(self.password, password)
        except:
            return False

    @classmethod
    def find_by_username(cls, username) -> UserModel:
        """ Find a user by username """
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userid(cls, _id) -> list[UserModel]:
        """ Fine a user by user_id """
        return cls.query.filter_by(id=_id).first()
