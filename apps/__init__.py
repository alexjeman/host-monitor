from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api

from apps.apikeys.views import api as apikeys_namespace
from apps.hosts.views import api as hosts_namespace
from config.settings import Settings

db = Settings.db
ma = Settings.ma

load_dotenv(verbose=True)

# Init Swagger API
api = Api(title='Host Monitor API', version='1.0.0',
          description='Host Monitor API',
          )

api.add_namespace(apikeys_namespace)
api.add_namespace(hosts_namespace)


# Init Flask create_app
def register_ext(new_app):
    db.init_app(new_app)
    ma.init_app(new_app)


def create_app():
    new_app = Flask(__name__)
    new_app.config.from_object(Settings())
    new_app.static_folder = new_app.config['STATIC_FOLDER']
    new_app.template_folder = new_app.config['TEMPLATES_FOLDER']
    register_ext(new_app)
    migrate = Migrate(db=db)
    migrate.init_app(app=new_app)
    api.init_app(app=new_app)
    return new_app
