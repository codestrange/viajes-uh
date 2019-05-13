from datetime import datetime
from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import state_blueprint
from .forms import CreateStateForm
from ...models import db, Comment, Concept, Country, Travel, State, Workflow, DocumentType, Role
from ...utils import flash_errors, user_can_decide


@state_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    form = CreateStateForm()
    form.upload.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.order_by(DocumentType.name).all()
    ]
    form.review.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.order_by(DocumentType.name).all()
    ]
    form.role.choices = [
        (str(role.id), role.name)
        for role in Role.query.order_by(Role.name).all()
    ]
    if form.validate_on_submit():
        state = State(name=form.name.data)
        upload = [ DocumentType.query.get_or_404(int(doc)) for doc in form.upload.data ]
        review = [ DocumentType.query.get_or_404(int(doc)) for doc in form.review.data ]
        role = [ Role.query.get_or_404(int(doc)) for doc in form.role.data ]
        state.need_uploaded = upload
        state.need_checked = review
        state.roles = role
        try:
            db.session.add(state)
            db.session.commit()
            flash('El estado ha sido creado correctamente.')
            return redirect(url_for('state._list'))
        except Exception as e:
            flash(f'Fecha invalida. {e}')
    else:
        flash_errors(form)
    return render_template('workflow/state.html', form=form)

@state_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    form = CreateStateForm()
    current = State.query.get_or_404(id)
    form.upload.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.order_by(DocumentType.name).all()
    ]
    form.review.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.order_by(DocumentType.name).all()
    ]
    form.role.choices = [
        (str(role.id), role.name)
        for role in Role.query.order_by(Role.name).all()
    ]
    if form.validate_on_submit():
        state = State(name=form.name.data)
        upload = [ DocumentType.query.get_or_404(int(doc)) for doc in form.upload.data ]
        review = [ DocumentType.query.get_or_404(int(doc)) for doc in form.review.data ]
        role = [ Role.query.get_or_404(int(doc)) for doc in form.role.data ]
        current.need_uploaded = upload
        current.need_checked = review
        current.roles = role
        try:
            db.session.add(current)
            db.session.commit()
            flash('El estado ha sido editado correctamente.')
            return redirect(url_for('state._list'))
        except Exception as e:
            flash(f'Fecha invalida. {e}')
    else:
        flash_errors(form)
    form.name.data = current.name
    form.upload.data = current.need_uploaded
    form.review.data = current.need_checked
    form.role.data = current.roles
    return render_template('workflow/edit_state.html', form=form)


@state_blueprint.route('/', methods=['GET'])
@login_required
def _list():
    states = State.query.all()
    return render_template('workflow/list_state.html', states=states)