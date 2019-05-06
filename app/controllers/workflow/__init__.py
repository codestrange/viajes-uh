from flask import Blueprint

workflow = Blueprint('workflow', __name__, template_folder='../../views')

from . import controllers
