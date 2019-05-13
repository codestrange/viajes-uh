from flask import abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import state_blueprint
from .forms import CreateStateForm, EditStateForm
from ...models import db, State, DocumentType, Role
from ...utils import flash_errors


@state_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_administrator and current_user.is_specialist:
        abort(403)
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
        upload = [DocumentType.query.get_or_404(int(doc)) for doc in form.upload.data]
        review = [DocumentType.query.get_or_404(int(doc)) for doc in form.review.data]
        role = [Role.query.get_or_404(int(doc)) for doc in form.role.data]
        state.need_uploaded = upload
        state.need_checked = review
        state.roles = role
        db.session.add(state)
        db.session.commit()
        flash('El estado ha sido creado correctamente.')
        return redirect(url_for('state.get_list'))
    else:
        flash_errors(form)
    return render_template('state/create.html', form=form)


@state_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_administrator and current_user.is_specialist:
        abort(403)
    form = EditStateForm()
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
        upload = [DocumentType.query.get_or_404(int(doc)) for doc in form.upload.data]
        review = [DocumentType.query.get_or_404(int(doc)) for doc in form.review.data]
        role = [Role.query.get_or_404(int(doc)) for doc in form.role.data]
        current.need_uploaded = upload
        current.need_checked = review
        current.roles = role
        db.session.add(current)
        db.session.commit()
        flash('El estado ha sido editado correctamente.')
        return redirect(url_for('state.get_list'))
    else:
        flash_errors(form)
    form.name.data = current.name
    form.upload.data = [str(doc.id) for doc in current.need_uploaded]
    form.review.data = [str(doc.id) for doc in current.need_checked]
    form.role.data = current.roles
    return render_template('state/edit.html', form=form)


@state_blueprint.route('/', methods=['GET'])
@login_required
def get_list():
    states = State.query.all()
    return render_template('state/list.html', states=states)
