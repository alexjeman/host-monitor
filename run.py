import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from apps import api
from config import db, ma

load_dotenv(verbose=True)


def register_ext(app):
    db.init_app(app)
    ma.init_app(app)


def create_app():
    new_app = Flask(__name__)
    new_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('SQLALCHEMY_DATABASE_URI')
    new_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    register_ext(new_app)
    migrate = Migrate(app=new_app, db=db)
    api.init_app(new_app)
    return new_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
