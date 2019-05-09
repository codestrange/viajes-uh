from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import approve_blueprint
from ...models import db, Travel
from ...utils import check_conditions, user_can_decide


@approve_blueprint.route('/travels')
@login_required
def approve_travels():
    travels = current_user.decisions()
    if not travels:
        return redirect(url_for('main.index'))
    return render_template('approve/list.html', travels=travels)


@approve_blueprint.route('/reject/travel/<int:id>', methods=['GET'])
@login_required
def reject_travel(id):
    if not user_can_decide(current_user, Travel.query.get(id)):
        return abort(403)
    travel = Travel.query.get(id)
    travel.rejected = True
    db.session.add(travel)
    db.session.commit()
    return redirect(url_for('approve.approve_travels'))


@approve_blueprint.route('/travel/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_travel_state(id):
    travel = Travel.query.get_or_404(id)
    if not user_can_decide(current_user, travel):
        return abort(403)
    documents = [
        document
        for document in travel.documents
        if travel.state.need_checked.filter_by(id=document.document_type.id).first()
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
    return render_template('approve/edit.html', travel=travel, documents=documents)
 