from . import api


@api.route('/users/', methods=['GET'])
def get_users():
    pass


@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    pass


@api.route('/users/', methods=['POST'])
def post_user():
    pass


@api.route('/users/<int:id>', methods=['PUT'])
def put_user(id):
    pass


@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    pass
