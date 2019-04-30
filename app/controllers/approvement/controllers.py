from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required
from . import approvement
from ...models import Travel

@approvement.route('/travels', methods=['GET'])
@login_required
def approve_travels():
    travels = [
        {
            'name': 'Mi viaje 1',
            'country': 'Cuba'
        },
        {
            'name': 'Mi viaje 2',
            'country': 'Canada'
        },
        {
            'name': 'Mi viaje 2',
            'country': 'Mexico'
        }
    ]
    return render_template('approvement/approve_travels.html', travels=travels)
