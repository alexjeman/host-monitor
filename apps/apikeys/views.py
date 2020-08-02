from flask import request
from flask_mail import Message
from flask_restx import Resource
from sqlalchemy import null
from apps.apikeys.models import ApiKey, db
from apps.apikeys.namespace import api, apikey_serializer, apikey_serializer_post, apikey_serializer_register, apikey_serializer_link
from apps.apikeys.security import encrypt, gen_new_key, get_owner
from apps.extensions import mail

NULL = null()


@api.route('/', methods=['GET', 'POST'])
class ApiKeyResource(Resource):
    @api.expect(apikey_serializer_post, validate=True)
    @api.doc('generate_apikey')
    @api.marshal_with(apikey_serializer_register, code=200)
    def post(self):
        generate_apikey = gen_new_key()

        try:
            is_telegram_request = request.json['chat_id']
        except:
            is_telegram_request = False

        if is_telegram_request:
            chat_id_exists = bool(ApiKey.query.filter_by(chat_id=request.json['chat_id']).first())
            if chat_id_exists:
                return "You are already registered.", 409
            pass

        else:
            check_exists = bool(ApiKey.query.filter_by(email=request.json['email']).first())
            if check_exists:
                return "Your email is already in.", 409

        new_apikey = ApiKey(
            apikey_hash=encrypt(generate_apikey),
            key=generate_apikey,
            email=request.json['email'] if not is_telegram_request else NULL,
            chat_id=request.json['chat_id'] if is_telegram_request else NULL
        )

        db.session.add(new_apikey)
        db.session.commit()
        if not is_telegram_request:
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

    @api.expect(apikey_serializer_link, validate=True)
    @api.doc('link_apikey', model=apikey_serializer)
    @api.marshal_with(apikey_serializer)
    def post(self, apikey):
        owner = get_owner(ApiKey, apikey)
        owner.chat_id = request.json['chat_id']
        db.session.add(owner)
        db.session.commit()
        return owner, 200
