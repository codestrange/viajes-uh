from flask import flash
from os import remove
from os.path import abspath, exists, join
from .models import db, Document, Travel, TypeDocument 


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


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{error}')
