from flask import flash
from os import remove
from os.path import abspath, exists, join
from .models import db, Document, Travel, DocumentType


def user_can_decide(user, travel):
    return travel.id in (trav.id for trav in user.decisions())


def user_can_decide_by_id(user, travel_id):
    return travel_id in (trav.id for trav in user.decisions())


def save_document(name, file_document, travel_id, document_type_id):
    travel = Travel.query.get(travel_id)
    document_type = DocumentType.query.get(document_type_id)
    document = Document(name=name, travel=travel, document_type=document_type)
    document.confirmed = True
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
    return document


def modify_document(document, name, file_document, travel_id, document_type_id):
    travel = Travel.query.get(travel_id)
    document_type = DocumentType.query.get(document_type_id)
    document.name = name
    document.confirmed = True
    document.travel = travel
    document.document_type = document_type
    file_name = str(document.id)
    file_name += f'.{file_document.filename.split(".")[-1]}' if file_document.filename.split(".") else ''
    path = join(f'{abspath("")}/app/static/uploads', file_name)
    document.path = join('uploads', file_name)
    db.session.add(document)
    db.session.commit()
    if exists(path):
        remove(path)
    file_document.save(path)
    return document


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}')
