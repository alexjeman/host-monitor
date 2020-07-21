from flask import jsonify
from flask_restx import Api, Resource

from models import User, user_schema
from settings import app

# Swagger API
api = Api(app, version='1.0.0', title='Host Monitor API',
          description='Host Monitor API',
          )
users_ns = api.namespace('users', description='Monitor users operations')


@users_ns.route('/<int:pk>/')
@users_ns.param('pk', 'User identifier')
class UsersResource(Resource):
    @users_ns.doc('get_user')
    def get(self, pk):
        user = User.query.filter_by(id=pk).first_or_404()
        return user_schema.dump(user)


if __name__ == '__main__':
    app.run(debug=True)
