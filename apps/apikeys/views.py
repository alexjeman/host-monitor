from flask import request
from flask_mail import Message
from flask_restx import Resource

from apps.apikeys.models import ApiKey, db
from apps.apikeys.namespace import api, apikey_serializer, apikey_serializer_post, apikey_serializer_register
from apps.apikeys.security import encrypt, gen_new_key, get_owner
from apps.extensions import mail


@api.route('/', methods=['GET', 'POST'])
class ApiKeyResource(Resource):
    @api.expect(apikey_serializer_post, validate=True)
    @api.doc('generate_apikey')
    @api.marshal_with(apikey_serializer_register, code=200)
    def post(self):
        generate_apikey = gen_new_key()
        check_exists = bool(ApiKey.query.filter_by(email=request.json['email']).first())
        if check_exists:
            return "You are already registered.", 409
        new_apikey = ApiKey(
            apikey_hash=encrypt(generate_apikey),
            email=request.json['email']
        )
        db.session.add(new_apikey)
        db.session.commit()
        if "@" in new_apikey.email:
            msg = Message("Your new API key has been generated",
                          sender="host@monitor.com",
                          recipients=[new_apikey.email],
                          body=f"A request has been made to create a new API key for your account.\n"
                               f"This API key is not recoverable, if you loose it, you should generate a new one.\n"
                               f"{generate_apikey}")
            mail.send(msg)
        new_apikey.apikey = generate_apikey
        return new_apikey, 200


@api.route('/<apikey>/')
@api.param('apikey', 'Your Api Key')
class ApiKeyResource(Resource):
    @api.doc('get_apikey_info', model=apikey_serializer)
    @api.marshal_with(apikey_serializer)
    def get(self, apikey):
        api_info = get_owner(ApiKey, apikey)
        return api_info
