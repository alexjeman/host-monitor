from apps.apikeys.security import verify_apikey
from apps.extensions import db


class ApiKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    apikey_hash = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=True)
    hosts = db.relationship('Hosts', backref='apikey', lazy=True)
    token = db.Column(db.String, unique=False, nullable=True)
    chat_id = db.Column(db.Integer, nullable=True)

    def check_apikey(self, api, apikey):
        return verify_apikey(api, apikey_hash=self.apikey_hash, apikey=apikey)

    def __init__(self, apikey_hash, email):
        self.apikey_hash = apikey_hash
        self.email = email
