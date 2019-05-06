from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import travel_mod
from ...models import db, User
from ...utils import flash_errors

@travel_mod.route('/<int:id>')
@login_required
def travel_viewer(id):
    return f"HELLO FROM THE OTHER SIDE WITH ID {id}."

