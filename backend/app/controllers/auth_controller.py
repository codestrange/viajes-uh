from flask import jsonify, g
from . import api
from ..auth import auth


@api.route('/token/')
@auth.login_required
def get_token():
    return jsonify({
        'id': g.current_user.id,
        'token': g.current_user.generate_auth_token()
    })
