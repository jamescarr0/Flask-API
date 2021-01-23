from flask_restful import Resource
from flask import request

from models.usermodel import UserModel


class UserRegister(Resource):
    def post(self) -> tuple[dict[str, str], int]:
        data = request.get_json()
        user = UserModel(data['username'], data['password'])

        if not user.username or not user.password:
            # No data sent - 400 Bad Request.
            return {"message": "Username and password required."}, 400
        elif UserModel.find_by_username(user.username):
            # User exists
            return {"message": "Username exists"}, 409

        user.save_to_db()
        return {"message": "User created successfully"}, 201
