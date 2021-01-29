from resources.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.verify_password(password):
        return user


def identity(payload):
    return UserModel.find_by_userid(payload['identity'])
