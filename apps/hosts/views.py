from flask import request
from flask_restx import Namespace, Resource, fields

from apps.hosts.models import Host, Stats, db
from apps.hosts.schemas import host_schema, stats_schema
from apps.apikeys.security import encrypt, gen_new_key

api = Namespace('hosts', description='Monitor host operations')

HostSerializer = api.model('HostSerializer', {
    'id': fields.Integer,
    'name': fields.String,
    'url': fields.String,
})

HostSerializerPost = api.model('HostSerializerPost', {
    'name': fields.String,
    'url': fields.String,
})

StatsSerializer = api.model('StatsSerializer', {
    'id': fields.Integer,
    'ping': fields.String,
    'time': fields.String,
})

StatsSerializerPost = api.model('StatsSerializerPost', {
    'ping': fields.String,
    'time': fields.String,
})


@api.route('/<apikey>/')
@api.param('apikey', 'ApiKey identifier')
class HostResource(Resource):
    @api.doc('add_host')
    @api.expect(HostSerializer)
    def post(self):
        new_host = HostSerializer(
            name=request.json['name'],
            url=request.json['url'],
        )
        db.session.add(new_host)
        db.session.commit()
        return host_schema.jsonify(new_host)


@api.route('/<apikey>/')
@api.param('apikey', 'ApiKey identifier')
class HostResource(Resource):
    @api.doc('get_host')
    @api.marshal_with(HostSerializer)
    def get(self, apikey):
        query = Host.query.filter_by(apikey=apikey)
        return host_schema.dump(query)
