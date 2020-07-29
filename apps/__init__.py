import atexit

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restx import Api
from apps.apikeys.views import api as apikey_namespace
from apps.bot.views import api as bot_namespace
from apps.extensions import db, mail
from apps.hosts.views import api as hosts_namespace
from config.settings import Settings


def ping_call():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
        "Upgrade-Insecure-Requests": "1", "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate"}
    requests.get('https://127.0.0.1:5000/hosts/ping-task/', timeout=60, headers=headers, verify=False)


def create_app():
    # Init Flask create_app
    new_app = Flask(__name__)
    new_app.config.from_object(Settings())
    new_app.static_folder = new_app.config['STATIC_FOLDER']
    new_app.template_folder = new_app.config['TEMPLATES_FOLDER']
    register_ext(new_app)
    CORS(new_app, resources={r"/*": {"origins": "*"}})
    migrate = Migrate(db=db)
    migrate.init_app(app=new_app)

    # Init Swagger API
    api = Api(title='Host Monitor API', version='1.0.0',
              description='Host Monitor API',
              )

    api.add_namespace(apikey_namespace)
    api.add_namespace(hosts_namespace)
    api.add_namespace(bot_namespace)
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
