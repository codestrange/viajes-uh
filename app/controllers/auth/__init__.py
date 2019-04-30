from flask import Blueprint

auth = Blueprint('auth', __name__, template_folder='../../views')

from . import controllers
