from flask import render_template
from flask_login import login_required
from . import main_blueprint


@main_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')


@main_blueprint.app_errorhandler(403)
def forbidden(e):
    return render_template('errors/403.html'), 403


@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404


@main_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500
