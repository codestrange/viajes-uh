from flask import Blueprint

state_blueprint = Blueprint('state', __name__, template_folder='../../views')

from . import controllers
