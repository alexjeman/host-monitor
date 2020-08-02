from flask_restx import Namespace, fields

from apps.hosts.namespace import host_serializer

api = Namespace('apikey', description='Monitor apikeys operations')

apikey_serializer = api.model('ApiKey', {
    'id': fields.Integer,
    'email': fields.String,
    'hosts': fields.Nested(host_serializer),
})

apikey_serializer_post = api.model('ApiKeyPost', {
    'email': fields.String,
})

apikey_serializer_link = api.model('ApiKeyLink', {
    'chat_id': fields.String,
})

apikey_serializer_register = api.model('ApiKeyRegister', {
    'email': fields.String,
    'apikey': fields.String,
})
