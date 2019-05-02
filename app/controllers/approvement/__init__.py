from flask import Blueprint

approvement = Blueprint('approvement', __name__, template_folder='../../views')

from . import controllers