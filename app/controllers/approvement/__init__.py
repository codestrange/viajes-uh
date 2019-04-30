from flask import Blueprint

approvement = Blueprint('approment', __name__, template_folder='../../views')

from . import controllers