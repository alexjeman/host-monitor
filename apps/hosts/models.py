from sqlalchemy.sql import func

from apps.extensions import db


class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, unique=False, nullable=True)
    muted = db.Column(db.Boolean, default=False, nullable=False)
    apikey_id = db.Column(db.Integer, db.ForeignKey('apikey.id'),
                          nullable=True)
    stats = db.relationship('Stats', backref='hosts', lazy=True)

    def __init__(self, url, apikey_id):
        self.url = url
        self.apikey_id = apikey_id


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, unique=False, nullable=True)
    response_time = db.Column(db.Integer, unique=False, nullable=True)
    time = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('hosts.id'),
                        nullable=True)

    def __init__(self, code, response_time, time, host_id):
        self.code = code
        self.response_time = response_time
        self.time = time
        self.host_id = host_id
