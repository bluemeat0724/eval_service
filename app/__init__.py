from flask import Flask
from flask_cors import CORS
from app.config import config
from app.models import db


cors = CORS()


def create_app(config_name):
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.config.from_object(config[config_name])
    db.init_app(app)

    from .api_1_0 import api
    app.register_blueprint(api)

    return app

