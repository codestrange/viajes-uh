from flask import g
from flask_httpauth import HTTPBasicAuth
from .errors import unauthorized as response_unauthorized
from .models.user import User


auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    g.current_user = User.query.filter_by(username=username).first()
    if g.current_user is None:
        return False
    return g.current_user.verify_password(password)


@auth.error_handler
def unauthorized():
    error_message = 'invalid password'
    if g.current_user is None:
        error_message = 'user don\'t exist'
    return response_unauthorized(error_message)


@auth_token.verify_password
def verify_auth_token(token, unused):
    g.current_user = User.verify_auth_token(token)
    return g.current_user is not None and unused == ''


@auth_token.error_handler
def unauthorized_token():
    return response_unauthorized('please send your authentication token')
