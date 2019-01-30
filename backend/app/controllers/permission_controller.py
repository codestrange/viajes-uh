from json import loads
from logging import exception
from flask import jsonify, abort, request
from . import api
from ..auth import auth_token
from ..container import Container
from ..exceptions import ValidationError
from ..entities.permission_entity import PermissionEntity


@api.route('/permissions/', methods=['GET'])
@auth_token.login_required
def get_permissions():
    repository = Container.instance().current_app.unitofwork.get_repository('PermissionRepository')
    permissions = repository.query().all()
    return jsonify([permission.to_json() for permission in permissions])


@api.route('/permissions/<int:id>/', methods=['GET'])
@auth_token.login_required
def get_permission(id):
    repository = Container.instance().current_app.unitofwork.get_repository('PermissionRepository')
    permission = repository.query().get(id)
    if permission is None:
        abort(404)
    return jsonify(permission.to_json())


@api.route('/permissions/', methods=['POST'])
@auth_token.login_required
def post_permission():
    repository = Container.instance().current_app.unitofwork.get_repository('PermissionRepository')
    json = loads(request.json) if isinstance(request.json, str) else request.json
    name = json.get('name')
    if name is None:
        raise ValidationError('Name is required.')
    if repository.query().filter(lambda x: x.name == name).first() is not None:
        raise ValidationError('Name already in use.')
    permission = PermissionEntity(name)
    repository.add(permission)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Permission created.'}), 201


@api.route('/permissions/<int:id>/', methods=['PUT'])
@auth_token.login_required
def put_permission(id):
    repository = Container.instance().current_app.unitofwork.get_repository('PermissionRepository')
    permission = repository.query().get(id)
    if permission is None:
        abort(404)
    json = loads(request.json) if isinstance(request.json, str) else request.json
    name = json.get('name')
    if name is None:
        raise ValidationError('Name is required.')
    if repository.query().filter(lambda x: x.name == name and x.id != id).first() is not None:
        raise ValidationError('Name already in use.')
    permission.name = name
    repository.add(permission)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Permission updated.'}), 201


@api.route('/permissions/<int:id>/', methods=['DELETE'])
@auth_token.login_required
def delete_permission(id):
    repository = Container.instance().current_app.unitofwork.get_repository('PermissionRepository')
    permission = repository.query().get(id)
    if permission is None:
        abort(404)
    repository.delete(permission)
    try:
        Container.instance().current_app.unitofwork.commit()
    except Exception as e:
        Container.instance().db.session.rollback()
        exception(e)
    return jsonify({'message': 'Permission deleted.'})
