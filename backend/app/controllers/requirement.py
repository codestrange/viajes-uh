from . import api


@api.route('/requirement/', methods=['GET'])
def get_requirements():
    pass


@api.route('/requirement/<int:id>', methods=['GET'])
def get_requirement():
    pass


@api.route('/requirement/', methods=['POST'])
def post_requirement():
    pass


@api.route('/requirement/<int:id>', methods=['PUT'])
def put_requirement():
    pass


@api.route('/requirement/<int:id>', methods=['DELETE'])
def delete_requirement():
    pass
