from . import api


@api.route('/permission/', methods=['GET'])
def get_permissions():
    pass


@api.route('/permission/<int:id>', methods=['GET'])
def get_permission():
    pass


@api.route('/permission/', methods=['POST'])
def post_permission():
    pass


@api.route('/permission/<int:id>', methods=['PUT'])
def put_permission():
    pass


@api.route('/permission/<int:id>', methods=['DELETE'])
def delete_permission():
    pass
