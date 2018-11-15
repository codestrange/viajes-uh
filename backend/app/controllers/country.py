from . import api


@api.route('/country/', methods=['GET'])
def get_countries():
    pass


@api.route('/country/<int:id>', methods=['GET'])
def get_country():
    pass


@api.route('/country/', methods=['POST'])
def post_country():
    pass


@api.route('/country/<int:id>', methods=['PUT'])
def put_country():
    pass


@api.route('/country/<int:id>', methods=['DELETE'])
def delete_country():
    pass
