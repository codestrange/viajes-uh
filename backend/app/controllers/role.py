from . import api


@api.route('/role/', methods=['GET'])
def get_roles():
    pass


@api.route('/role/<int:id>', methods=['GET'])
def get_role():
    pass


@api.route('/role/', methods=['POST'])
def post_role():
    pass


@api.route('/role/<int:id>', methods=['PUT'])
def put_role():
    pass


@api.route('/role/<int:id>', methods=['DELETE'])
def delete_role():
    pass
