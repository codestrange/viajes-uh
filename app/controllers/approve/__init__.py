from flask import Blueprint

approve_blueprint = Blueprint('approve', __name__, template_folder='../../views')

from . import controllers
