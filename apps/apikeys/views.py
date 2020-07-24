from flask import request
from flask_restx import Resource

from apps.apikeys.models import ApiKey, db
from apps.apikeys.namespace import api, apikey_serializer, apikey_serializer_post, apikey_serializer_register
from apps.apikeys.security import encrypt, gen_new_key, get_owner


@api.route('/', methods=['GET', 'POST'])
class ApiKeyResource(Resource):
    @api.expect(apikey_serializer_post, validate=True)
    @api.doc('generate_apikey')
    @api.marshal_with(apikey_serializer_register, code=201)
    def post(self):
        generate_apikey = gen_new_key()
        new_apikey = ApiKey(
            apikey_hash=encrypt(generate_apikey),
            email=request.json['email']
        )
        db.session.add(new_apikey)
        db.session.commit()
        new_apikey.apikey = generate_apikey
        return new_apikey, 201


@api.route('/<apikey>/')
@api.param('apikey', 'Your Api Key')
class ApiKeyResource(Resource):
    @api.doc('get_apikey_info', model=apikey_serializer)
    @api.marshal_with(apikey_serializer)
    def get(self, apikey):
        api_info = get_owner(ApiKey, apikey)
        return api_info
