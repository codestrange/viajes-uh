from os import getenv
from app import create_app
from app.models import db, Area, Concept,  Comment, Country, Document, Region, Role, Travel, \
    TypeDocument, User, WorkflowState

app = create_app(getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Area=Area, Concept=Concept, Comment=Comment, Country=Country, \
                Document=Document, Region=Region, Role=Role, Travel=Travel, \
                TypeDocument=TypeDocument, User=User, WorkflowState=WorkflowState)


@app.cli.command()
def init():
    insert(Area)
    insert(Concept)
    insert(Country)
    insert(TypeDocument)
    insert(User)
    insert(Role)
    insert(WorkflowState)
    insert(Travel)
    insert(Document)


def insert(model):
    print(f'Inserting table {model.__tablename__} ...')
    model.insert()
    print(f'Table {model.__tablename__} inserted - OK')
