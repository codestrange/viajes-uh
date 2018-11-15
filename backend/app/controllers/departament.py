from . import api


@api.route('/departament/', methods=['GET'])
def get_departaments():
    pass


@api.route('/departament/<int:id>', methods=['GET'])
def get_departament():
    pass


@api.route('/departament/', methods=['POST'])
def post_departament():
    pass


@api.route('/departament/<int:id>', methods=['PUT'])
def put_departament():
    pass


@api.route('/departament/<int:id>', methods=['DELETE'])
def delete_departament():
    pass
