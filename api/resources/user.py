from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from api.models.usermodel import UserModel


class UserRegister(Resource):
    """
    UserRegister resource endpoint - manages new user registration requests.
    """

    def post(self) -> tuple[dict[str, str], int]:
        """ Responds to the User registration POST request. """

        # Get request data.
        data = request.get_json()

        # Check request data for username and password.
        if not data['username'] or not data['password']:
            # No data sent.
            return {"message": "Username and password required."}, 400
        elif UserModel.find_by_username(data['username']):
            # User exists
            return {"message": "Username exists"}, 409

        # Create a new user and save to database.
        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        # User registration successful.
        return {"message": "User created successfully"}, 201


class User(Resource):
    """
    User resource end points.
    """

    @classmethod
    @jwt_required
    def get(cls, user_id):
        """ Responds to the User GET request """

        # Retrieve user by user id.
        user = UserModel.find_by_userid(user_id)
        # Return user details if user found else return message.
        return (user.json(), 200) if user else ({'message': 'User not found'}, 404)

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        """ Responds to the User DELETE request """

        # Retrieve user by user id.
        user = UserModel.find_by_userid(user_id)
        if user:
            # If user exists, delete user and return confirmation.
            user.delete()
            return {'message': 'user deleted'}, 200

        # User does not exist.
        return {'message': 'user not found'}, 404


class UserLogin(Resource):
    """
    UserLogin class manages the logging in of registered users returning access and refresh tokens
    for authentication when accessing protected resources / end points.
    """

    @classmethod
    def post(cls):
        """ Responds to the UserLogin POST request """

        # Get the request data.
        data = request.get_json()

        # Retrieve requested username from database.
        user = UserModel.find_by_username(data['username'])

        # Check user exists and verify password hash.
        if user and user.verify_password(data['password']):
            # If credentials correct, return access & refresh tokens.
            return {
                'access_token': create_access_token(identity=user.id, fresh=True),
                'refresh_token': create_refresh_token(user.id)
            }, 200

        # username or password invalid.
        return {'message': 'Invalid credentials'}, 401
