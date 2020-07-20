import settings
from settings import app
from models import db, User
from flask import jsonify


@app.route('/')
def show_user():
    users = User.query.filter_by(username='Flask').first_or_404()
    body = {
        "id": users.id,
        "username": users.username,
        "email": users.email
    }
    return jsonify(body)


if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
