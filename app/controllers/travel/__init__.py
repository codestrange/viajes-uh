from flask import Blueprint

travel_blueprint = Blueprint('travel', __name__, template_folder='../../views')

from . import controllers
