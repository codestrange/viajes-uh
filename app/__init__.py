from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .admin import admin, AreaProdModelView, ComentProdModelView, ConceptProdModelView, \
    CountryProModelView, DocumentProdModelView, DocumentTypeProdModelView, IndexProdModelView, \
    RegionProdModelType, RoleProdModelType, StateProdModelView, TravelProdModelView, \
    UserProdModelView, WorkflowProdModelView
from .config import config
from .models import Area, Comment, Concept, Country, Document, DocumentType, Index, Region, Role, \
    State, Travel, User, Workflow, db, login_manager

migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    admin.add_view(AreaProdModelView(Area, db.session, endpoint='areaAdmin'))
    admin.add_view(ComentProdModelView(Comment, db.session, endpoint='commentAdmin'))
    admin.add_view(ConceptProdModelView(Concept, db.session, endpoint='conceptAdmin'))
    admin.add_view(CountryProModelView(Country, db.session, endpoint='countryAdmin'))
    admin.add_view(DocumentProdModelView(Document, db.session, endpoint='documentAdmin'))
    admin.add_view(DocumentTypeProdModelView(DocumentType, db.session, endpoint='typeAdmin'))
    admin.add_view(IndexProdModelView(Index, db.session, endpoint='indexAdmin'))
    admin.add_view(RegionProdModelType(Region, db.session, endpoint='regionAdmin'))
    admin.add_view(RoleProdModelType(Role, db.session, endpoint='roleAdmin'))
    admin.add_view(StateProdModelView(State, db.session, endpoint='stateAdmin'))
    admin.add_view(TravelProdModelView(Travel, db.session, endpoint='travelAdmin'))
    admin.add_view(UserProdModelView(User, db.session, endpoint='userAdmin'))
    admin.add_view(WorkflowProdModelView(Workflow, db.session, endpoint='workflowAdmin'))

    from .controllers.main import main_blueprint
    app.register_blueprint(main_blueprint)

    from .controllers.approve import approve_blueprint
    app.register_blueprint(approve_blueprint, url_prefix='/approve')

    from .controllers.auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .controllers.document import document_blueprint
    app.register_blueprint(document_blueprint, url_prefix='/document')

    from .controllers.travel import travel_blueprint
    app.register_blueprint(travel_blueprint, url_prefix='/travel')

    from .controllers.workflow import state_blueprint
    app.register_blueprint(state_blueprint, url_prefix='/state')

    return app
