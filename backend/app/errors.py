from flask import jsonify
from app.exceptions import ValidationError
from .controllers import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    return response, 400


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    return response, 401


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    return response, 403


@api.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
