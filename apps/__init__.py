import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api

from apps.apikeys.views import api as apikeys_namespace
from config import db, ma

load_dotenv(verbose=True)

# Init Swagger API
api = Api(title='Host Monitor API', version='1.0.0',
          description='Host Monitor API',
          )

api.add_namespace(apikeys_namespace)


# Init Flask create_app
def register_ext(new_app):
    db.init_app(new_app)
    ma.init_app(new_app)


def create_app():
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    register_ext(new_app)
    migrate = Migrate(db=db)
    migrate.init_app(app=new_app)
    api.init_app(app=new_app)
    return new_app
