from datetime import datetime
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import travel_blueprint
from .forms import CreateTravelForm, CommentForm
from ...models import db, Comment, Concept, Country, Travel
from ...utils import flash_errors


@travel_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateTravelForm()
    form.concept.choices = [
        (str(concept.id), concept.name)
        for concept in Concept.query.order_by(Concept.name).all()
    ]
    form.country.choices = [
        (str(country.id), country.name)
        for country in Country.query.order_by(Country.name).all()
    ]
    if form.validate_on_submit():
        travel = Travel(name=form.name.data)
        travel.user = current_user
        concept = Concept.query.get_or_404(int(form.concept.data))
        country = Country.query.get_or_404(int(form.country.data))
        travel.concept = concept
        travel.country = country
        travel.duration = form.duration.data
        travel.workflow_state = country.workflow_state
        hour = int(form.departure_date_hour.data)
        minute = int(form.departure_date_minute.data)
        day = int(form.departure_date_day.data)
        month = int(form.departure_date_month.data)
        year = int(form.departure_date_year.data)
        try:
            _datetime =  datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            travel.departure_date = _datetime
            db.session.add(travel)
            db.session.commit()
            flash('Su viaje ha sido creado correctamente.')
            return redirect(request.args.get('next') or url_for('main.index'))
        except Exception as e:
            flash(f'Fecha invalida. {e}')
    else:
        flash_errors(form)
    return render_template('travel/create.html', form=form)


@travel_blueprint.route('/', methods=['GET'])
@login_required
def travels():
    return render_template('travel/list.html', travels=current_user.travels)


@travel_blueprint.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def get(id):
    if id not in (travel.id for travel in current_user.travels):
        abort(403)
    travel = Travel.query.get(id)
    requirements = []
    for requirement in travel.workflow_state.requirements.all():
        mask = False
        for document in travel.documents.all():
            if document.type_document.id == document.id:
                mark = True
                break
        if not mask:
            requirements.append(requirement)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.text = form.text.data
        comment.user = current_user
        comment.travel = travel
        db.session.add(comment)
        db.session.commit()
        form.text.data = ''
    else:
        flash_errors(form)
    return render_template('travel/view.html', travel=travel, requirements=requirements, form=form)
