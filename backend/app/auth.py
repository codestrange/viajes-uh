from flask import g
from flask_httpauth import HTTPBasicAuth
from .container import Container
from .errors import unauthorized as response_unauthorized
from .entities.user_entity import UserEntity


auth = HTTPBasicAuth()
auth_token = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    g.current_user = repository.query().filter(lambda user: user.username == username).first()
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
    g.current_user = UserEntity.verify_auth_token(token)
    return g.current_user is not None and unused == ''


@auth_token.error_handler
def unauthorized_token():
    return response_unauthorized('please send your authentication token')
