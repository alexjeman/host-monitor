import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(object):
    # Flask config
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    STATIC_FOLDER = os.path.join(BASE_DIR, 'static')
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, 'templates')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEBUG = DEBUG
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    DEFAULT_MAIL_SENDER = os.getenv('DEFAULT_MAIL_SENDER')

    # Swagger UI config
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True
    SWAGGER_UI_DOC_EXPANSION = 'list'
