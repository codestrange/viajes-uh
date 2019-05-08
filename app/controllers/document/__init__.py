from flask import Blueprint

document = Blueprint('document', __name__, template_folder='../../views')

from . import controllers
