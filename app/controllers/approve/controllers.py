from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required
from . import approve
from ...models import db, Travel, User, Country, Document, WorkflowState

@approve.route('/travels', methods=['GET'])
@login_required
def approve_travels():
    return render_template('approve/approve_travels.html', travels=current_user.decisions())

@approve.route('/travels/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_travel_state(id):
    travel = Travel.query.get(id)
    creator = User.query.get(travel.user_id)
    to_country = Country.query.get(travel.country_id)
    state = WorkflowState.query.get(travel.workflow_state_id)
    documents = travel.documents
    requirements_ids = [ requirement.id for requirement in state.requirements ]
    requirements = [ requirement for requirement in state.requirements ]
    to_confirm_documents = [ document for document in documents if document.type_id in requirements_ids ]
    if request.method == 'POST':
        confirmed_docs = [ Document.query.get(int(id)) for id in request.form.getlist('confirmed_docs') ]
        confirmed_ids = { doc.id for doc in confirmed_docs }
        for doc in confirmed_docs:
            doc.confirmed = True
            db.session.add(doc)
        for doc in [ document for document in documents if document.id not in confirmed_ids ]:
            doc.confirmed = False
            db.session.add(doc)
        db.session.commit()
    return render_template('approve/edit_travel.html', \
    travel=travel, \
    creator=creator, \
    to_country=to_country, \
    documents=to_confirm_documents, \
    requirements=requirements)
 
