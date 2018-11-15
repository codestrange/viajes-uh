from . import api


@api.route('/travel/', methods=['GET'])
def get_travels():
    pass


@api.route('/travel/<int:id>', methods=['GET'])
def get_travel():
    pass


@api.route('/travel/', methods=['POST'])
def post_travel():
    pass


@api.route('/travel/<int:id>', methods=['PUT'])
def put_travel():
    pass


@api.route('/travel/<int:id>', methods=['DELETE'])
def delete_travel():
    pass
