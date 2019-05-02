from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required
from . import approve
from ...models import Travel


@approve.route('/travels')
@login_required
def approve_travels():
    return render_template('approve/approve_travels.html', travels=current_user.decisions())


@approve.route('/travels/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_travel_state(id):
    return render_template('approve/edit_travel.html', travel=Travel.query.get(id))
 
