from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__, template_folder='../../views')

from . import controllers
