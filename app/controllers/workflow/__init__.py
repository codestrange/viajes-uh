from flask import Blueprint

workflow_blueprint = Blueprint('workflow', __name__, template_folder='../../views')

from . import controllers
