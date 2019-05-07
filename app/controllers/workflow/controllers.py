from flask import redirect, render_template, request, url_for
from . import workflow
from .forms import AppendWorkflowStateForm, CreateWorkflowStateForm, EditWorkflowStateForm
from ...models import db, Role, TypeDocument, WorkflowState
from ...utils import flash_errors


@workflow.route('/view/<int:id>', methods=['GET'])
def view_workflow(id):
    workflow_actual = WorkflowState.query.get_or_404(id)
    return render_template('workflow/view.html', workflow=workflow_actual)


@workflow.route('/create', methods=['GET', 'POST'])
def create_workflow():
    form = CreateWorkflowStateForm()
    requirements = TypeDocument.query.all()
    roles = Role.query.all()
    next_nodes = WorkflowState.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    form.next_node.choices = [('0', 'Seleccione un nodo siguiente')] + \
        [(str(next_node.id), next_node.name) for next_node in next_nodes]
    if form.validate_on_submit():
        new_workflow = WorkflowState(name=form.name.data)
        new_workflow.role = Role.query.get(form.role.data)
        for item in form.requirements.data:
            new_workflow.requirements.append(TypeDocument.query.get(int(item)))
        if form.next_node.data != '0':
            new_workflow.next_id = int(form.next_node.data)
        db.session.add(new_workflow)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.view_workflow', id=new_workflow.id))
    else:
        flash_errors(form)
    return render_template('workflow/create.html', form=form)


@workflow.route('/append/<int:id>', methods=['GET', 'POST'])
def append_workflow(id=0):
    prev_workflow = WorkflowState.query.get_or_404(id)
    form = AppendWorkflowStateForm()
    requirements = TypeDocument.query.all()
    roles = Role.query.all()
    next_nodes = WorkflowState.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    if form.validate_on_submit():
        new_workflow = WorkflowState(name=form.name.data)
        new_workflow.role = Role.query.get(form.role.data)
        for item in form.requirements.data:
            new_workflow.requirements.append(TypeDocument.query.get(int(item)))
        db.session.add(new_workflow)
        db.session.commit()
        prev_workflow.next_id = new_workflow.id
        db.session.add(prev_workflow)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.append_workflow', id=new_workflow.id))
    else:
        flash_errors(form)
    return render_template('workflow/append.html', form=form, prev_workflow=prev_workflow)


@workflow.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_workflow(id):
    workflow_actual = WorkflowState.query.get_or_404(id)
    form = EditWorkflowStateForm()
    requirements = TypeDocument.query.all()
    roles = Role.query.all()
    next_nodes = WorkflowState.query.all()
    form.requirements.choices = [(str(requirement.id), requirement.name) 
                                    for requirement in requirements]
    form.role.choices = [(str(role.id), role.name) for role in roles]
    form.next_node.choices = [('0', 'Seleccione un nodo siguiente')] + \
        [(str(next_node.id), next_node.name) for next_node in next_nodes]
    form.name.data = workflow_actual.name
    form.role.data = str(workflow_actual.role.id)
    form.next_node.data = str(workflow_actual.next_id) if workflow_actual.next_id else '0'
    form.requirements.data = []
    for requirement in workflow_actual.requirements.all():
        form.requirements.data.append(str(requirement.id))
    if form.validate_on_submit():
        workflow_actual.name = form.name.data
        workflow_actual.role = Role.query.get(form.role.data)
        workflow_actual.requirements = []
        for item in form.requirements.data:
            workflow_actual.requirements.append(TypeDocument.query.get(int(item)))
        if form.next_node.data != '0':
            workflow_actual.next_id = int(form.next_node.data)
        db.session.add(workflow_actual)
        db.session.commit()
        return redirect(request.args.get('next') or \
            url_for('workflow.view_workflow', id=workflow_actual.id))
    else:
        flash_errors(form)
    return render_template('workflow/edit.html', form=form)


@workflow.route('/', methods=['GET'])
def get_workflows():
    workflows = WorkflowState.query.all()
    return render_template('workflow/workflows.html', workflows=workflows)


@workflow.route('/<int:id>', methods=['GET'])
def graph_workflow(id):
    workflows = [WorkflowState.query.get_or_404(id)]
    for workflow in workflows:
        if workflow.next:
            workflows.append(workflow.next)
    return render_template('workflow/graph.html',
                           start_workflow=workflows[0],
                           end_workflow=workflows[-1],
                           workflows=workflows)
