from flask import flash
from os import remove
from os.path import abspath, exists, join
from .models import db, Document, Travel, TypeDocument, WorkflowState 


def save_document(name, file_document, travel_id, type_document_id):
    travel = Travel.query.get(travel_id)
    type_document = TypeDocument.query.get(type_document_id)
    document = Document(name=name, travel=travel, type_document=type_document)
    db.session.add(document)
    db.session.commit()
    file_name = str(document.id)
    file_name += f'.{file_document.filename.split(".")[-1]}' if file_document.filename.split(".") else ''
    path = join(f'{abspath("")}/app/static/uploads', file_name)
    document.path = path
    db.session.add(document)
    db.session.commit()
    if exists(path):
        remove(path)
    file_document.save(path)


def check_conditions(travel):
    actual_state = WorkflowState.query.get(travel.workflow_state_id)
    documents = travel.documents
    requirements_ids = [ requirement.id for requirement in actual_state.requirements ]
    to_confirm_documents = [ document for document in documents if document.type_id in requirements_ids ]
    if travel.confirmed_in_state:
        for requirement in requirements_ids:
            for doc in to_confirm_documents:
                if doc.type_id == requirement and doc.confirmed:
                    break
            else:
                return False
        travel.confirmed_in_state = False
        if actual_state.next_id:
            travel.workflow_state_id = actual_state.next_id
        else:
            travel.accepted = True
        db.session.add(travel)
        db.session.commit()
        return True
    return False


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}')
