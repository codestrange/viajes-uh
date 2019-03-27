from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .admin import admin, ModelView, UserModelView
from .config import config
from .database import db, Permission, Role, User

migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    admin.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    admin.add_view(ModelView(Permission, db.session))
    admin.add_view(ModelView(Role, db.session))
    admin.add_view(UserModelView(User, db.session))

    from .controllers import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
