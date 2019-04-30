from flask import Blueprint

main = Blueprint('main', __name__, template_folder='../../views')

from . import controllers
