from . import api


@api.route('/career/', methods=['GET'])
def get_careers():
    pass


@api.route('/career/<int:id>', methods=['GET'])
def get_career():
    pass


@api.route('/career/', methods=['POST'])
def post_career():
    pass


@api.route('/career/<int:id>', methods=['PUT'])
def put_career():
    pass


@api.route('/career/<int:id>', methods=['DELETE'])
def delete_career():
    pass
