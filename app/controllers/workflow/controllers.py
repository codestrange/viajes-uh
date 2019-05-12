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
            return redirect(url_for('main.index'))
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
            flash('El estado ha sido creado correctamente.')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Fecha invalida. {e}')
    else:
        flash_errors(form)
    form.name.data = current.name
    form.upload.data = current.need_uploaded
    form.review.data = current.need_checked
    form.role.data = current.roles
    return render_template('workflow/edit_state.html', form=form)


# @travel_blueprint.route('/', methods=['GET'])
# @login_required
# def travels():
#     return render_template('travel/list.html', travels=current_user.travels)


# @travel_blueprint.route('/<int:id>', methods=['GET', 'POST'])
# @login_required
# def get(id):
#     travel = Travel.query.get(id)
#     if id not in (_travel.id for _travel in current_user.travels) and \
#         not user_can_decide(current_user, travel):
#         abort(403)
#     need_checkeds = []
#     for need_checked in travel.state.need_checked.all():
#         mask = False
#         for document in travel.documents.all():
#             if document.document_type.id == document.id and not document.upload_by_node:
#                 mark = True
#                 break
#         if not mask:
#             need_checkeds.append(need_checked)
#     need_uploadeds = []
#     for need_uploaded in travel.state.need_uploaded.all():
#         mask = False
#         for document in travel.documents.all():
#             if document.document_type.id == document.id and document.upload_by_node:
#                 mark = True
#                 break
#         if not mask:
#             need_uploadeds.append(need_uploaded)
#     form = CommentForm()
#     if form.validate_on_submit():
#         comment = Comment()
#         comment.text = form.text.data
#         comment.user = current_user
#         comment.travel = travel
#         db.session.add(comment)
#         db.session.commit()
#         form.text.data = ''
#     else:
#         flash_errors(form)
#     comments = travel.comments.all()
#     comments.reverse()
#     return render_template('travel/view.html', travel=travel, need_checkeds=need_checkeds,
#                            need_uploadeds=need_uploadeds, comments=comments, form=form)
