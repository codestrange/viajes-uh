from flask import redirect, render_template, url_for
from . import workflow_blueprint
from .forms import CreateForm, EditForm, InsertForm
from ...models import db, Index, State, Workflow
from ...utils import flash_errors


@workflow_blueprint.route('/', methods=['GET'])
def get_list():
    workflows = Workflow.query.all()
    return render_template('workflow/list.html', workflows=workflows)


@workflow_blueprint.route('/edit/<int:id>', methods=['GET'])
def edit(id):
    workflow = Workflow.query.get_or_404(id)
    states = [index.state for index in workflow.states.order_by(Index.index)]
    return render_template('workflow/edit.html', workflow=workflow, states=states)


@workflow_blueprint.route('/insert/<int:id>/<int:index>', methods=['GET', 'POST'])
def insert(id, index):
    form = InsertForm()
    form.state.choices = [(str(state.id), state.name) for state in State.query.all()]
    if form.validate_on_submit():
        workflow = Workflow.query.get_or_404(id)
        state = State.query.get_or_404(int(form.state.data))
        Workflow.insert_state(workflow, state, index)
        return redirect(url_for('workflow.edit', id=id))
    else:
        flash_errors(form)
    return render_template('workflow/insert.html', form=form)


@workflow_blueprint.route('/remove/<int:id>/<int:index>', methods=['GET'])
def remove(id, index):
    workflow = Workflow.query.get_or_404(id)
    Workflow.remove_state(workflow, index)
    return redirect(url_for('workflow.edit', id=id))


@workflow_blueprint.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateForm()
    if form.validate_on_submit():
        workflow = Workflow(name=form.name.data)
        db.session.add(workflow)
        db.session.commit()
        return redirect(url_for('workflow.get_list'))
    else:
        flash_errors(form)
    return render_template('workflow/create.html', form=form)


@workflow_blueprint.route('/edit_info/<int:id>', methods=['GET', 'POST'])
def edit_info(id):
    workflow = Workflow.query.get_or_404(id)
    form = EditForm()
    if form.validate_on_submit():
        workflow.name = form.name.data
        db.session.add(workflow)
        db.session.commit()
        return redirect(url_for('workflow.get_list'))
    else:
        flash_errors(form)
    form.name.data = workflow.name
    return render_template('workflow/edit_info.html', form=form)
