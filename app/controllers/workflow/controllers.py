from flask import abort, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from . import workflow_blueprint
from .forms import AppendStateForm, CreateStateForm, EditStateForm
from ...models import db, Role, DocumentType, State
from ...utils import flash_errors


@workflow_blueprint.route('/view/<int:id>', methods=['GET'])
@login_required
def view(id):
    if not current_user.is_specialist:
        abort(403)
    workflow = State.query.get_or_404(id)
    return render_template('workflow/view.html', workflow=workflow_actual)


@workflow_blueprint.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not current_user.is_specialist:
        abort(403)
    form = CreateStateForm()
    requirements = DocumentType.query.all()
    roles = Role.query.all()
    next_nodes = State.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    form.next_node.choices = [('0', 'Seleccione un nodo siguiente')] + \
        [(str(next_node.id), next_node.name) for next_node in next_nodes]
    if form.validate_on_submit():
        new_workflow = State(name=form.name.data)
        new_workflow.role = Role.query.get(form.role.data)
        for item in form.requirements.data:
            new_workflow.need_checked.append(DocumentType.query.get(int(item)))
        # if form.next_node.data != '0':
            # new_workflow.next_id = int(form.next_node.data)
        db.session.add(new_workflow)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.view_workflow', id=new_workflow.id))
    else:
        flash_errors(form)
    return render_template('workflow/create.html', form=form)


@workflow_blueprint.route('/append/<int:id>', methods=['GET', 'POST'])
@login_required
def append(id=0):
    if not current_user.is_specialist:
        abort(403)
    prev_workflow = State.query.get_or_404(id)
    form = AppendStateForm()
    requirements = DocumentType.query.all()
    roles = Role.query.all()
    next_nodes = State.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    if form.validate_on_submit():
        new_workflow = State(name=form.name.data)
        new_workflow.role = Role.query.get(form.role.data)
        for item in form.requirements.data:
            new_workflow.need_checked.append(DocumentType.query.get(int(item)))
        db.session.add(new_workflow)
        db.session.commit()
        # prev_workflow.next_id = new_workflow.id
        db.session.add(prev_workflow)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.append_workflow', id=new_workflow.id))
    else:
        flash_errors(form)
    return render_template('workflow/append.html', form=form, prev_workflow=prev_workflow)


@workflow_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    if not current_user.is_specialist:
        abort(403)
    workflow_actual = State.query.get_or_404(id)
    form = EditStateForm()
    requirements = DocumentType.query.all()
    roles = Role.query.all()
    next_nodes = State.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    form.next_node.choices = [('0', 'Seleccione un nodo siguiente')] + \
        [(str(next_node.id), next_node.name) for next_node in next_nodes]
    form.name.data = workflow_actual.name
    # form.role.data = str(workflow_actual.role.id)
    # form.next_node.data = str(workflow_actual.next_id) if workflow_actual.next_id else '0'
    form.requirements.data = []
    for requirement in workflow_actual.requirements.all():
        form.requirements.data.append(str(requirement.id))
    if form.validate_on_submit():
        workflow_actual.name = form.name.data
        # workflow_actual.role = Role.query.get(form.role.data)
        # workflow_actual.requirements = []
        for item in form.requirements.data:
            workflow_actual.need_checked.append(DocumentType.query.get(int(item)))
        # if form.next_node.data != '0':
            # workflow_actual.next_id = int(form.next_node.data)
        db.session.add(workflow_actual)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.view_workflow', id=workflow_actual.id))
    else:
        flash_errors(form)
    return render_template('workflow/edit.html', form=form)


@workflow_blueprint.route('/', methods=['GET'])
@login_required
def get():
    if not current_user.is_specialist:
        abort(403)
    workflows = State.query.all()
    return render_template('workflow/workflows.html', workflows=workflows)


@workflow_blueprint.route('/<int:id>', methods=['GET'])
@login_required
def graph(id):
    if not current_user.is_specialist:
        abort(403)
    workflows = [State.query.get_or_404(id)]
    # for workflow in workflows:
        # if workflow.next:
            # workflows.append(workflow.next)
    return render_template('workflow/graph.html',
                           start_workflow=workflows[0],
                           end_workflow=workflows[-1],
                           workflows=workflows)
