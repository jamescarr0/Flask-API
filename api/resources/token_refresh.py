from flask_restful import Resource
from flask_jwt_extended import jwt_refresh_token_required, get_jwt_identity, create_access_token


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Refreshes a logged in users access token.
        Token returned is NOT fresh.
        """

        # Get the current logged in users identity
        current_user = get_jwt_identity()

        # Create a new access token that is NOT fresh as a means to not annoy the user. (Users are not prompted to
        # enter login details again).
        # For security purposes, actions such as performing a password change would require a FRESH token
        # and be prompted to login again - providing valid username and password credentials for increased security.
        return {'access_token': create_access_token(identity=current_user, fresh=False)}, 200
