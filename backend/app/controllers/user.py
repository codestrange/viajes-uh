from . import api


@api.route('/user/', methods=['GET'])
def get_users():
    pass


@api.route('/user/<int:id>', methods=['GET'])
def get_user():
    pass


@api.route('/user/', methods=['POST'])
def post_user():
    pass


@api.route('/user/<int:id>', methods=['PUT'])
def put_user():
    pass


@api.route('/user/<int:id>', methods=['DELETE'])
def delete_user():
    pass
