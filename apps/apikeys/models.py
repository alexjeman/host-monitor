from apps.apikeys.security import verify_apikey
from apps.extensions import db


class ApiKey(db.Model):
    __tablename__ = 'apikey'
    id = db.Column(db.Integer, primary_key=True)
    apikey_hash = db.Column(db.String, unique=True, nullable=True)
    email = db.Column(db.String, unique=True, nullable=True)
    hosts = db.relationship('Hosts', backref='apikey', lazy=True)
    key = db.Column(db.String, unique=True, nullable=False)
    chat_id = db.Column(db.Integer, unique=True, nullable=True)

    def check_apikey(self, api, apikey):
        return verify_apikey(api, apikey_hash=self.apikey_hash, apikey=apikey)

    def __init__(self, apikey_hash, key, email, chat_id):
        self.apikey_hash = apikey_hash
        self.key = key
        self.email = email
        self.chat_id = chat_id
