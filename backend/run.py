from os import getenv
from app import create_app
from app.database import db, Area, Country, Document, Region, Role, Travel, TypeDocument, User, \
    WorkflowState

app = create_app(getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Area=Area, Country=Country, Document=Document, Region=Region, \
                Role=Role, Travel=Travel, TypeDocument=TypeDocument, User=User, \
                WorkflowState=WorkflowState)


@app.cli.command()
def init():
    pass
