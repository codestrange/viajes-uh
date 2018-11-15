from . import api


@api.route('/academy/', methods=['GET'])
def get_academies():
    pass


@api.route('/academy/<int:id>', methods=['GET'])
def get_academy():
    pass


@api.route('/academy/', methods=['POST'])
def post_academy():
    pass


@api.route('/academy/<int:id>', methods=['PUT'])
def put_academy():
    pass


@api.route('/academy/<int:id>', methods=['DELETE'])
def delete_academy():
    pass
