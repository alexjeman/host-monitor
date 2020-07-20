from flask_sqlalchemy import SQLAlchemy

from settings import app

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)


# db.session.add(User(username="Flask", email="example@example.com"))
# db.session.commit()
