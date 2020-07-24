from flask_restx import Namespace, fields

api = Namespace('hosts', description='Monitor host operations')

host_serializer = api.model('HostSerializer', {
    'id': fields.Integer,
    'apikey_id': fields.Integer,
    'name': fields.String,
    'url': fields.String,
})

host_serializer_post = api.model('HostSerializerPost', {
    'name': fields.String,
    'url': fields.String,
})

stats_serializer = api.model('StatsSerializer', {
    'id': fields.Integer,
    'code': fields.String,
    'response_time': fields.String,
    'time': fields.String,
    'host_id': fields.String,
})

stats_serializer_post = api.model('StatsSerializerPost', {
    'ping': fields.String,
    'time': fields.String,
})
