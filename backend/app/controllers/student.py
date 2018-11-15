from . import api


@api.route('/student/', methods=['GET'])
def get_students():
    pass


@api.route('/student/<int:id>', methods=['GET'])
def get_student():
    pass


@api.route('/student/', methods=['POST'])
def post_student():
    pass


@api.route('/student/<int:id>', methods=['PUT'])
def put_student():
    pass


@api.route('/student/<int:id>', methods=['DELETE'])
def delete_student():
    pass
