from flask import jsonify, request, g
from . import api
from ..auth import auth, auth_simple, auth_token, generate_auth_token, \
    generate_confirmation_token, verify_confirmation_token
from ..database import db, User,Travel
from ..errors import bad_request
from ..utils import check_json, json_load



@api.route('/travel', methods=['POST'])
def post_travel():
    user_id = g.current_user.id
    json = json_load(request.json)
    check_json(json, ['name', 'country_id'])
    #actualizar el workflow_state a travez de la tabla country
    travel = Travel(name=json.name, user_id=user_id, country_id=json.country_id)

    db.session.add(travel)
    db.session.commit()
    token = generate_confirmation_token(travel)
    print(f'\nToken: {token}\n')
    # send email
    return jsonify({'message': 'Viaje registrado aún sin confirmar.'}), 201