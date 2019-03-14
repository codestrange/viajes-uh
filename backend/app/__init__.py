from flask import Flask
from flask_cors import CORS
from .admin import admin, ModelView, UserModelView
from .config import config
from .database import db, Career, City, Country, Department, Faculty, Institution, Permission, \
    Procedure, Process, Role, Student, Teacher, Transition, Travel, User, Workflow


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app)
    db.init_app(app)

    admin.add_view(ModelView(Career, db.session, category='Users'))
    admin.add_view(ModelView(City, db.session, category='Workflows'))
    admin.add_view(ModelView(Country, db.session, category='Workflows'))
    admin.add_view(ModelView(Department, db.session, category='Users'))
    admin.add_view(ModelView(Faculty, db.session, category='Users'))
    admin.add_view(ModelView(Institution, db.session, category='Workflows'))
    admin.add_view(ModelView(Permission, db.session, category='Users'))
    admin.add_view(ModelView(Procedure, db.session, category='Workflows'))
    admin.add_view(ModelView(Process, db.session, category='Workflows'))
    admin.add_view(ModelView(Role, db.session, category='Users'))
    admin.add_view(ModelView(Student, db.session, category='Users'))
    admin.add_view(ModelView(Teacher, db.session, category='Users'))
    admin.add_view(ModelView(Transition, db.session, category='Workflows'))
    admin.add_view(ModelView(Travel, db.session, category='Workflows'))
    admin.add_view(UserModelView(User, db.session, category='Users'))
    admin.add_view(ModelView(Workflow, db.session, category='Workflows'))

    from .controllers import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
