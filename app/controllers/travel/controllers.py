from datetime import datetime
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import travel_blueprint
from .forms import CreateTravelForm, CommentForm
from ...models import db, Comment, Concept, Country, Travel, State, Workflow
from ...utils import flash_errors, user_can_decide


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
        travel.justification = form.justification.data
        if current_user.category == 'employee':
            travel.workflow = travel.country.region.workflow_employee
        elif current_user.category == 'student':
            travel.workflow = travel.country.region.workflow_student
        else:
            travel.workflow = travel.country.region.workflow_teacher
        Workflow.move(travel)
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
    travel = Travel.query.get(id)
    if id not in (_travel.id for _travel in current_user.travels) and \
        not user_can_decide(current_user, travel):
        abort(403)
    need_checkeds = []
    for need_checked in travel.state.need_checked.all():
        mask = False
        for document in travel.documents.all():
            if document.document_type.id == document.id and not document.upload_by_node:
                mark = True
                break
        if not mask:
            need_checkeds.append(need_checked)
    need_uploadeds = []
    for need_uploaded in travel.state.need_uploaded.all():
        mask = False
        for document in travel.documents.all():
            if document.document_type.id == document.id and document.upload_by_node:
                mark = True
                break
        if not mask:
            need_uploadeds.append(need_uploaded)
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
    return render_template('travel/view.html', travel=travel, need_checkeds=need_checkeds,
                           need_uploadeds=need_uploadeds, form=form)
