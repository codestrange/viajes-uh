from flask import Blueprint

document_blueprint = Blueprint('document', __name__, template_folder='../../views')

from . import controllers
