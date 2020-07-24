import atexit

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate
from flask_restx import Api

from apps.apikeys.views import api as apikey_namespace
from apps.extensions import db, mail
from apps.hosts.views import api as hosts_namespace
from config.settings import Settings

load_dotenv(verbose=True)


def ping_call():
    requests.get('http://127.0.0.1:5000/hosts/ping-task/', timeout=60)


def create_app():
    # Init Flask create_app
    new_app = Flask(__name__)
    new_app.config.from_object(Settings())
    new_app.static_folder = new_app.config['STATIC_FOLDER']
    new_app.template_folder = new_app.config['TEMPLATES_FOLDER']
    register_ext(new_app)
    migrate = Migrate(db=db)
    migrate.init_app(app=new_app)

    # Init Swagger API
    api = Api(title='Host Monitor API', version='1.0.0',
              description='Host Monitor API',
              )

    api.add_namespace(apikey_namespace)
    api.add_namespace(hosts_namespace)
    api.init_app(app=new_app)

    # APScheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=ping_call, trigger="interval", seconds=300)

    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return new_app


# Register extensions
def register_ext(new_app):
    db.init_app(new_app)
    mail.init_app(new_app)
