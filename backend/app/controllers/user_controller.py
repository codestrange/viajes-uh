from flask import jsonify, abort
from . import api
from ..container import Container


@api.route('/users/', methods=['GET'])
def get_users():
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    users = repository.query().all()
    return jsonify([user.to_json() for user in users])


@api.route('/users/<int:id>/', methods=['GET'])
def get_user(id):
    repository = Container.instance().current_app.unitofwork.get_repository('UserRepository')
    user = repository.query().get(id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@api.route('/users/', methods=['POST'])
def post_user():
    pass


@api.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    pass


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
