from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from settings import app

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email')


user_schema = UserSchema()
users_schema = UserSchema(many=True)