from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import travel_mod
from ...models import db, User, Travel
from ...utils import flash_errors


@travel_mod.route('/')
@login_required
def travels_view():
    _user = current_user
    return render_template("travel/travels.html", _user=_user)

@travel_mod.route('/<int:id>')
@login_required
def travel_viewer(id):
    _travel = Travel.query.get(id)
    return render_template("travel/travel.html", _travel=_travel)