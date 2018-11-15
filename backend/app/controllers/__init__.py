from flask import Blueprint

api = Blueprint('api', __name__)

from . import academy, career, country, departament, faculty, \
    permission, requirement, role, student, teacher, travel, user
