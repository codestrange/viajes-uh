from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, login_required
from . import approve
from ...models import db, Travel, User, Country, Document, WorkflowState, Role
from ...utils import check_conditions, user_can_decide


@approve.route('/travels')
@login_required
def approve_travels():
    travels = current_user.decisions()
    if not travels:
        return redirect(url_for('main.index'))
    return render_template('approve/approve_travels.html', travels=travels)


@approve.route('/reject/travel/<int:id>', methods=['GET'])
@login_required
def reject_travel(id):
    if not user_can_decide(current_user, Travel.query.get(id)):
        return abort(403)
    travel = Travel.query.get(id)
    travel.rejected = True
    db.session.add(travel)
    db.session.commit()
    return redirect(url_for('approve.approve_travels'))


@approve.route('/travel/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_travel_state(id):
    if not user_can_decide(current_user, Travel.query.get(id)):
        return abort(403)
    travel = Travel.query.get(id)
    creator = User.query.get(travel.user_id)
    to_country = Country.query.get(travel.country_id)
    state = WorkflowState.query.get(travel.workflow_state_id)
    role = Role.query.get(state.role_id)
    documents = travel.documents
    requirements_ids = [ requirement.id for requirement in state.requirements ]
    requirements = [ requirement for requirement in state.requirements ]
    to_confirm_documents = [ document for document in documents if document.type_id in requirements_ids ]
    if request.method == 'POST':
        confirmed_docs = [ Document.query.get(int(id)) for id in request.form.getlist('confirmed_docs') ]
        confirmed_ids = { doc.id for doc in confirmed_docs }
        if request.form.get('accept_travel'):
            travel.confirmed_in_state = True
            db.session.add(travel)
        for doc in confirmed_docs:
            doc.confirmed = True
            db.session.add(doc)
        for doc in [ document for document in documents if document.id not in confirmed_ids ]:
            doc.confirmed = False
            db.session.add(doc)
        db.session.commit()
        if check_conditions(travel):
            return redirect(url_for('approve.approve_travels'))
    return render_template('approve/edit_travel.html', \
    travel=travel, \
    creator=creator, \
    to_country=to_country, \
    documents=to_confirm_documents, \
    requirements=requirements, \
    role=role )
 
