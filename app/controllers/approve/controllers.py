from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, current_user, login_required
from . import approve
from ...models import db, Travel, User, Country, Document, WorkflowState, Role, TypeDocument
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
    travel = Travel.query.get_or_404(id)
    if not user_can_decide(current_user, travel):
        return abort(403)
    documents = [
        document
        for document in travel.documents
        if travel.workflow_state.requirements.filter_by(id=document.type_document.id).first()
    ]
    if request.method == 'POST':
        confirmed = {int(id) for id in request.form.getlist('confirmed_docs')}
        if request.form.get('accept_travel'):
            travel.confirmed_in_state = True
            db.session.add(travel)
        for document in documents:
            document.confirmed = document.id in confirmed
            db.session.add(document)
        db.session.commit()
        if check_conditions(travel):
            return redirect(url_for('approve.approve_travels'))
    return render_template('approve/edit_travel.html', travel=travel, documents=documents)
 