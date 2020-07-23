import uuid

from flask import request
from flask_restx import Namespace, Resource, fields

from apps.apikeys.models import ApiKey, db
from apps.apikeys.schemas import apikey_schema
from apps.apikeys.security import encrypt

api = Namespace('apikey', description='Monitor apikeys operations')

ApiKeySerializerGet = api.model('ApiKeySerializerGet', {
    'id': fields.Integer,
    'email': fields.String,
    'apikey': fields.String,
    'apikey_hash': fields.String,
})

ApiKeySerializerPost = api.model('ApiKeySerializerPost', {
    'email': fields.String,
})


@api.route('/', methods=['GET', 'POST'])
class UsersResource(Resource):
    @api.doc('generate_apikey')
    @api.expect(ApiKeySerializerPost)
    def post(self):
        generate_apikey = str(uuid.uuid4())
        new_apikey = ApiKey(
            apikey=generate_apikey,
            apikey_hash=encrypt(generate_apikey),
            email=request.json['email']
        )
        db.session.add(new_apikey)
        db.session.commit()
        return apikey_schema.jsonify(new_apikey)


@api.route('/<apikey>/')
@api.param('apikey', 'ApiKey identifier')
class UsersResource(Resource):
    @api.doc('get_apikey')
    @api.marshal_with(ApiKeySerializerGet)
    def get(self, apikey):
        query = ApiKey.query.filter_by(apikey=apikey).first_or_404()
        is_valid_apikey = query.check_apikey(apikey)
        print(is_valid_apikey)
        return apikey_schema.dump(query)
