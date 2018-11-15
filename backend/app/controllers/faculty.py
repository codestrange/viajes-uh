from . import api


@api.route('/faculty/', methods=['GET'])
def get_faculties():
    pass


@api.route('/faculty/<int:id>', methods=['GET'])
def get_faculty():
    pass


@api.route('/faculty/', methods=['POST'])
def post_faculty():
    pass


@api.route('/faculty/<int:id>', methods=['PUT'])
def put_faculty():
    pass


@api.route('/faculty/<int:id>', methods=['DELETE'])
def delete_faculty():
    pass
