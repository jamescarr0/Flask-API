#############################################
# Customised JWT Extended error callbacks  #
#############################################

from api.auth import jwt


def _response(msg: str, err: str, status_code=401) -> tuple[dict[str, str], int]:
    """
    Returns a custom JSON error response

    Args:
        msg: 'Generic message for useful feedback the user.'
        err: 'Error information for user feedback'
    Returns:
        JSON error message.
    """
    return {
               'message': msg,
               'error': err
           }, status_code


@jwt.expired_token_loader
def expired_token_callback(error) -> tuple[dict[str, str], int]:
    """ Returns a custom message for when the Token has expired """
    return _response(msg='Token has expired', err=error['type'])


@jwt.invalid_token_loader
def invalid_token_callback() -> tuple[dict[str, str], int]:
    """ Request header contains invalid JWT data. """
    return _response('Signature verification failed', 'invalid_token')


@jwt.unauthorized_loader
def unauthorised_callback(error) -> tuple[dict[str, str], int]:
    """ No JWT sent in request header """
    return _response('Request does not contain an access token', error)


@jwt.needs_fresh_token_loader
def fresh_token_required_callback() -> tuple[dict[str, str], int]:
    """ Non-fresh token used to access a resource that requires a FRESH token. """
    return _response('The token is not fresh', 'fresh_token_required')


@jwt.revoked_token_loader
def token_revoked_callback() -> tuple[dict[str, str], int]:
    """ Token revoked error message """
    return _response('This token has been revoked', 'token_revoked')
