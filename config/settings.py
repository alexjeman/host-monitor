import os

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


class Settings(object):
    # Flask config
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db = SQLAlchemy()
    ma = Marshmallow()
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Swagger UI config
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
