import datetime
from apps.extensions import db


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    apikey_id = db.Column(db.Integer, db.ForeignKey('apikey.id'),
                          nullable=False)
    stats = db.relationship('Stats', backref='hosts', lazy=True)

    def __init__(self, name, url, apikey_id):
        self.name = name
        self.url = url
        self.apikey_id = apikey_id


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=False, nullable=False)
    response_time = db.Column(db.Float, unique=False, nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'),
                        nullable=False)

    def __init__(self, code, response_time, host_id):
        self.code = code
        self.response_time = response_time
        self.host_id = host_id