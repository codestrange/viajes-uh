from flask import Blueprint

travel_mod = Blueprint('travel_mod', __name__, template_folder='../../views')

from . import controllers
