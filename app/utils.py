from flask import flash
from os import remove
from os.path import abspath, exists, join
from .models import db, Document, Travel, TypeDocument, WorkflowState


def user_can_decide(user, travel):
    return travel.id in (trav.id for trav in user.decisions())


def save_document(name, file_document, travel_id, type_document_id):
    travel = Travel.query.get(travel_id)
    type_document = TypeDocument.query.get(type_document_id)
    document = Document(name=name, travel=travel, type_document=type_document)
    db.session.add(document)
    db.session.commit()
    file_name = str(document.id)
    file_name += f'.{file_document.filename.split(".")[-1]}' if file_document.filename.split(".") else ''
    path = join(f'{abspath("")}/app/static/uploads', file_name)
    document.path = join('uploads', file_name)
    db.session.add(document)
    db.session.commit()
    if exists(path):
        remove(path)
    file_document.save(path)


def modify_document(document, name, file_document, travel_id, type_document_id):
    travel = Travel.query.get(travel_id)
    type_document = TypeDocument.query.get(type_document_id)
    document.name = name
    document.travel = travel
    document.type_document = type_document
    file_name = str(document.id)
    file_name += f'.{file_document.filename.split(".")[-1]}' if file_document.filename.split(".") else ''
    path = join(f'{abspath("")}/app/static/uploads', file_name)
    document.path = join('uploads', file_name)
    db.session.add(document)
    db.session.commit()
    if exists(path):
        remove(path)
    file_document.save(path)


def check_conditions(travel):
    documents = [
        document
        for document in travel.documents
        if travel.workflow_state.requirements.filter_by(id=document.type_document.id).first()
    ]
    if travel.confirmed_in_state:
        for requirement in travel.workflow_state.requirements:
            for document in documents:
                if document.type_document.id == requirement.id and document.confirmed:
                    break
            else:
                return False
        travel.confirmed_in_state = False
        if travel.workflow_state.next:
            travel.workflow_state = travel.workflow_state.next
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
