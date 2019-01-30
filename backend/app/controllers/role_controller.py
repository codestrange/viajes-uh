from json import loads
from logging import exception
from flask import jsonify, abort, request
from . import api
from ..auth import auth_token
from ..container import Container
from ..exceptions import ValidationError
from ..entities.role_entity import RoleEntity


@api.route('/roles/', methods=['GET'])
@auth_token.login_required
def get_roles():
    repository = Container.instance().current_app.unitofwork.get_repository('RoleRepository')
    roles = repository.query().all()
    return jsonify([role.to_json() for role in roles])


@api.route('/roles/<int:id>/', methods=['GET'])
@auth_token.login_required
def get_role(id):
    repository = Container.instance().current_app.unitofwork.get_repository('RoleRepository')
    role = repository.query().get(id)
    if role is None:
        abort(404)
    return jsonify(role.to_json())


@api.route('/roles/', methods=['POST'])
@auth_token.login_required
def post_role():
    repository = Container.instance().current_app.unitofwork.get_repository('RoleRepository')
    json = loads(request.json) if isinstance(request.json, str) else request.json
    name = json.get('name')
    if name is None:
        raise ValidationError('Name is required.')
    if repository.query().filter(lambda x: x.name == name).first() is not None:
        raise ValidationError('Name already in use.')
    role = RoleEntity(name)
    repository.add(role)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Role created.'}), 201


@api.route('/roles/<int:id>/', methods=['PUT'])
@auth_token.login_required
def put_role(id):
    repository = Container.instance().current_app.unitofwork.get_repository('RoleRepository')
    role = repository.query().get(id)
    if role is None:
        abort(404)
    json = loads(request.json) if isinstance(request.json, str) else request.json
    name = json.get('name')
    if name is None:
        raise ValidationError('Name is required.')
    if repository.query().filter(lambda x: x.name == name and x.id != id).first() is not None:
        raise ValidationError('Name already in use.')
    role.name = name
    repository.add(role)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Role updated.'}), 201


@api.route('/roles/<int:id>/', methods=['DELETE'])
@auth_token.login_required
def delete_role(id):
    repository = Container.instance().current_app.unitofwork.get_repository('RoleRepository')
    role = repository.query().get(id)
    if role is None:
        abort(404)
    repository.delete(role)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Role deleted.'})
