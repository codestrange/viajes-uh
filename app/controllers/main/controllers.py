from datetime import datetime
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from . import main
from .forms import CreateTravelForm, UploadDocumentForm
from ...models import db, Concept, Country, Travel, TypeDocument
from ...utils import flash_errors, save_document


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/create_travel', methods=['GET', 'POST'])
@login_required
def create_travel():
    form = CreateTravelForm()
    form.concept.choices = [(str(concept.id), concept.name) for concept in Concept.query.order_by(Concept.name).all()]
    form.country.choices = [(str(country.id), country.name) for country in Country.query.order_by(Country.name).all()]
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
    return render_template('create_travel.html', form=form)


@main.route('/upload_document', methods=['GET', 'POST'])
@login_required
def upload_document():
    form = UploadDocumentForm()
    form.travel.choices = [
        (str(travel.id), travel.name)
        for travel in Travel.query.filter(Travel.user_id == current_user.id).all()
    ]
    form.type_document.choices = [
        (str(type_document.id), type_document.name)
        for type_document in TypeDocument.query.all()
    ]
    if form.validate_on_submit():
        save_document(form.name.data, form.file_document.data, form.travel.data,
                      form.type_document.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('upload_document.html', form=form)
