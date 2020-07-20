import os

from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

# Read .env file, parse the contents
load_dotenv(verbose=True)

DEBUG = True

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DATABASE_URI')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


