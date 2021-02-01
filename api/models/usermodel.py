from argon2 import PasswordHasher

from api.db import db


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    # Create password hashing object. No params passed will use Argon2 Default values.
    ph = PasswordHasher()

    def __init__(self, username, password):
        self.username = username
        self.password = self.ph.hash(password)

    def __repr__(self):
        return f"<User: _id: {self.id}, username: {self.username}>"

    def json(self):
        return {
            'id': self.id,
            'username': self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def verify_password(self, password):
        try:
            return self.ph.verify(self.password, password)
        except:
            return False

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_userid(cls, _id):
        return cls.query.filter_by(id=_id).first()