from flask import Blueprint

approve = Blueprint('approve', __name__, template_folder='../../views')

from . import controllers