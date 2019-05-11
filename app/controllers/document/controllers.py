from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import document_blueprint
from .forms import EditDocumentForm, UploadDocumentForm
from ...models import db, Document, DocumentType, Travel
from ...utils import flash_errors, modify_document, save_document


@document_blueprint.route('/upload/<int:id>', methods=['GET', 'POST'])
@login_required
def upload(id):
    form = UploadDocumentForm()
    travel = Travel.query.get_or_404(id)
    if not travel.id in (t.id for t in current_user.decisions()):
        abort(403)
    form.document_type.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.all()
        if document_type.id in (dt.id for dt in travel.state.need_uploaded.all())
    ]
    if form.validate_on_submit():
        document = save_document(form.name.data, form.file_document.data, travel.id,
                                 form.document_type.data)
        document.user = current_user
        document.upload_by_node = True
        db.session.add(document)
        db.session.commit()
        document.travel.log(f'Subio el documento {document} de tipo {document.document_type}.', current_user)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('document/upload.html', form=form)


@document_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    document = Document.query.get_or_404(id)
    if document.user.id != current_user.id or document.confirmed:
        abort(403)
    if document.travel.accepted or document.travel.rejected or document.travel.cancelled:
        abort(404)
    form = EditDocumentForm()
    form.name.data = document.name
    if form.validate_on_submit():
        document = modify_document(document, form.name.data, form.file_document.data, document.travel.id,
                                   document.document_type.id)
        document.confirmed = True
        db.session.add(document)
        db.session.commit()
        document.travel.log(f'Resubio el documento {document} de tipo {document.document_type}.', current_user)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    return render_template('document/edit.html', form=form)


@document_blueprint.route('/edit_auth/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_auth(id):
    document = Document.query.get_or_404(id)
    if not document.travel.id in (t.id for t in current_user.decisions()):
        abort(403)
    if not document.upload_by_node:
        abort(403)
    if document.travel.accepted or document.travel.rejected or document.travel.cancelled:
        abort(404)
    form = UploadDocumentForm()
    form.document_type.choices = [
        (str(document_type.id), document_type.name)
        for document_type in DocumentType.query.all()
        if document_type.id in (dt.id for dt in document.travel.state.need_uploaded.all())
    ]
    if form.validate_on_submit():
        document = modify_document(document, form.name.data, form.file_document.data, document.travel.id,
                                   document.document_type.id)
        document.confirmed = True
        db.session.add(document)
        db.session.commit()
        document.travel.log(f'Resubio el documento {document} de tipo {document.document_type}.', current_user)
        return redirect(request.args.get('next') or url_for('main.index'))
    else:
        flash_errors(form)
    form.name.data = document.name
    form.document_type.data = document.document_type.id
    return render_template('document/edit_auth.html', form=form)


@document_blueprint.route('/rejecteds')
@login_required
def see_rejecteds():
    documents = current_user.rejected_documents()
    return render_template('document/rejecteds.html', documents=documents)
