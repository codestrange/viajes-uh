from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_required
from . import document_blueprint
from .forms import UploadDocumentForm
from ...models import Document, DocumentType, Travel
from ...utils import flash_errors, modify_document, save_document, user_can_decide_by_id


@document_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadDocumentForm()
    ids = [
        travel.id
        for travel in Travel.query.filter(Travel.user_id == current_user.id).all()
    ]
    ids += [ travel.id for travel in current_user.decisions() if not travel.id in ids]
    travels = [Travel.query.get(_id) for _id in ids]
    form.travel.choices = [
        (str(travel.id), travel.name)
        for travel in travels if not travel.accepted and not travel.rejected
    ]
    form.document_type.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.all()
    ]
    if form.validate_on_submit():
        save_document(form.name.data, form.file_document.data, form.travel.data,
                      form.document_type.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('document/upload.html', form=form)


@document_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    document = Document.query.get_or_404(id)
    if document.travel.accepted or document.travel.rejected:
        abort(404)
    form = UploadDocumentForm()
    ids = [
        travel.id
        for travel in Travel.query.filter(Travel.user_id == current_user.id).all()
    ]
    ids += [ travel.id for travel in current_user.decisions() if not travel.id in ids]
    travels = [Travel.query.get(_id) for _id in ids]
    form.travel.choices = [
        (str(travel.id), travel.name)
        for travel in travels if not travel.accepted and not travel.rejected
    ]
    form.document_type.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.all()
    ]
    form.name.data = document.name
    form.travel.data = str(document.travel.id)
    form.document_type.data = str(document.document_type.id)
    if form.validate_on_submit():
        modify_document(document, form.name.data, form.file_document.data, form.travel.data,
                      form.document_type.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('document/edit.html', form=form)
