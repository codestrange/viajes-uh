from flask import Flask
from flask_cors import CORS
from .config import config
from .database import Database

db = Database()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    from .controllers import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
