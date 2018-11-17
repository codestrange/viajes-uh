from flask import jsonify, abort
from . import api
from ..models.user import User


@api.route('/users/', methods=['GET'])
def get_users():
    users = User.query().all()
    return jsonify([user.to_json() for user in users])


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query().get(id)
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
