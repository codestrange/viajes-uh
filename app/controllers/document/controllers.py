from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_required
from . import document_blueprint
from .forms import UploadDocumentForm
from ...models import Document, Travel, TypeDocument
from ...utils import flash_errors, modify_document, save_document


@document_blueprint.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadDocumentForm()
    form.travel.choices = [
        (str(travel.id), travel.name)
        for travel in Travel.query.filter(Travel.user_id == current_user.id).all()
        if not travel.accepted and not travel.rejected
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
    return render_template('document/upload.html', form=form)


@document_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    document = Document.query.get_or_404(id)
    form = UploadDocumentForm()
    form.travel.choices = [
        (str(travel.id), travel.name)
        for travel in Travel.query.filter(Travel.user_id == current_user.id).all()
        if not travel.accepted and not travel.rejected
    ]
    form.type_document.choices = [
        (str(type_document.id), type_document.name)
        for type_document in TypeDocument.query.all()
    ]
    form.name.data = document.name
    form.travel.data = str(document.travel.id)
    form.type_document.data = str(document.type_document.id)
    if form.validate_on_submit():
        modify_document(document, form.name.data, form.file_document.data, form.travel.data,
                      form.type_document.data)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('document/edit.html', form=form)
