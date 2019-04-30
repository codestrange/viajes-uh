from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user
from . import main
from .forms import CreateTravelForm
from ...models import db, Country, Travel


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/create_travel', methods=['GET', 'POST'])
@login_required
def create_travel():
    form = CreateTravelForm()
    form.country.choices = [(str(country.id), country.name) for country in Country.query.order_by(Country.name).all()]
    if form.validate_on_submit():
        travel = Travel(name=form.name.data)
        travel.user = current_user
        country = Country.query.get_or_404(int(form.country.data))
        travel.country = country
        travel.workflow_state = country.workflow_state
        db.session.add(travel)
        db.session.commit()
        flash('Su viaje ha sido creado correctamente.')
        return redirect(request.args.get('next') or url_for('main.index'))
    return render_template('create_travel.html', form=form)
