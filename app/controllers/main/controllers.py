from flask import render_template
from flask_login import login_required
from . import main_blueprint


@main_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')
