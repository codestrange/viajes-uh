from os import getenv
from app import create_app
from app.models import Area, Comment, Concept, Country, Document, DocumentType, Region, Role, State, \
    Travel, User, Workflow, db

app = create_app(getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, Area=Area, Comment=Comment, Concept=Concept, Country=Country, \
                Document=Document, DocumentType=DocumentType, Region=Region, Role=Role, \
                State=State, Travel=Travel, User=User, Workflow=Workflow, db=db)


@app.cli.command()
def init():
    insert(Area)
    insert(Concept)
    insert(Country)
    insert(DocumentType)
    insert(Role)
    insert(User)
    insert(State)
    insert(Travel)
    insert(Document)


def insert(model):
    print(f'Inserting table {model.__tablename__} ...')
    model.insert()
    print(f'Table {model.__tablename__} inserted - OK')
