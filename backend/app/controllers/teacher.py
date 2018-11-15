from . import api


@api.route('/teacher/', methods=['GET'])
def get_teachers():
    pass


@api.route('/teacher/<int:id>', methods=['GET'])
def get_teacher():
    pass


@api.route('/teacher/', methods=['POST'])
def post_teacher():
    pass


@api.route('/teacher/<int:id>', methods=['PUT'])
def put_teacher():
    pass


@api.route('/teacher/<int:id>', methods=['DELETE'])
def delete_teacher():
    pass
