from flask import request
from flask_restx import Namespace, Resource, fields

from apps.apikeys.models import ApiKey, db
from apps.apikeys.schemas import apikey_schema
from apps.apikeys.security import encrypt, gen_new_key

api = Namespace('apikey', description='Monitor apikeys operations')

ApiKeySerializer = api.model('ApiKeySerializer', {
    'id': fields.Integer,
    'email': fields.String,
    'apikey': fields.String,
    'apikey_hash': fields.String,
})

ApiKeySerializerPost = api.model('ApiKeySerializerPost', {
    'email': fields.String,
})


@api.route('/', methods=['GET', 'POST'])
class ApiKeyResource(Resource):
    @api.doc('generate_apikey')
    @api.expect(ApiKeySerializerPost)
    def post(self):
        generate_apikey = gen_new_key()
        new_apikey = ApiKey(
            apikey=generate_apikey,
            apikey_hash=encrypt(generate_apikey),
            email=request.json['email']
        )
        db.session.add(new_apikey)
        db.session.commit()
        return apikey_schema.jsonify(new_apikey)


@api.route('/<apikey>/')
@api.param('apikey', 'Your Api Key')
class ApiKeyResource(Resource):
    @api.doc('get_apikey')
    @api.marshal_with(ApiKeySerializer)
    def get(self, apikey):
        query = ApiKey.query.filter_by(apikey=apikey).first_or_404()
        is_valid_apikey = query.check_apikey(apikey)
        print(is_valid_apikey)
        return apikey_schema.dump(query)
