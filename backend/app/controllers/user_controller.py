from json import loads
from logging import exception
from flask import jsonify, abort, request
from . import api
from ..auth import auth_token
from ..container import Container
from ..exceptions import ValidationError
from ..entities.user_entity import UserEntity


@api.route('/users/', methods=['GET'])
@auth_token.login_required
def get_users():
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    users = repository.query().all()
    return jsonify([user.to_json() for user in users])


@api.route('/users/<int:id>/', methods=['GET'])
@auth_token.login_required
def get_user(id):
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    user = repository.query().get(id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@api.route('/users/', methods=['POST'])
@auth_token.login_required
def post_user():
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    json = loads(request.json) if isinstance(request.json, str) else request.json
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')
    if None in (username, email, password):
        raise ValidationError('Username, Email and Password are required.')
    if repository.query().filter(lambda x: x.username == username).first() is not None:
        raise ValidationError('Username already in use.')
    if repository.query().filter(lambda x: x.email == email).first() is not None:
        raise ValidationError('Email already registered.')
    user = UserEntity(username, email, password)
    repository.add(user)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'User registered.'}), 201


@api.route('/users/<int:id>/', methods=['PUT'])
@auth_token.login_required
def put_user(id):
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    user = repository.query().get(id)
    if user is None:
        abort(404)
    json = loads(request.json) if isinstance(request.json, str) else request.json
    username = json.get('username')
    email = json.get('email')
    password = json.get('password')
    if None in (username, email, password):
        raise ValidationError('Username, Email and Password are required.')
    if repository.query().filter(lambda x: x.username == username and x.id != id).first() is not None:
        raise ValidationError('Username already in use.')
    if repository.query().filter(lambda x: x.email == email and x.id != id).first() is not None:
        raise ValidationError('Email already registered.')
    user.username = username
    user.email = email
    user.password = password
    repository.add(user)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'User updated.'}), 201


@api.route('/users/<int:id>/', methods=['DELETE'])
@auth_token.login_required
def delete_user(id):
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    user = repository.query().get(id)
    if user is None:
        abort(404)
    repository.delete(user)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'User deleted.'})
