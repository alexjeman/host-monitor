from flask import request, abort
from flask_restx import Resource
import requests
from requests import exceptions

from apps.apikeys.models import ApiKey
from apps.apikeys.security import get_owner
from apps.hosts.models import Hosts, Stats, db
from apps.hosts.namespace import api, host_serializer, host_serializer_post, stats_serializer


@api.route('/<apikey>/')
@api.param('apikey', 'Your Api Key')
class HostResource(Resource):
    @api.doc('get_hosts')
    @api.marshal_with(host_serializer)
    def get(self, apikey):
        owner = get_owner(ApiKey, apikey)
        hosts = Hosts.query.filter_by(apikey_id=owner.id).all()
        return hosts

    @api.expect(host_serializer_post)
    @api.doc('add_host')
    @api.marshal_with(host_serializer, code=201)
    def post(self, apikey):
        owner = get_owner(ApiKey, apikey)
        try:
            requests.get(request.json['url'], timeout=60)
        except exceptions.ConnectionError:
            return abort(400, 'This host does not seem to exist, please enter a different host.')

        new_host = Hosts(
            apikey_id=owner.id,
            name=request.json['name'],
            url=request.json['url'],
        )
        db.session.add(new_host)
        db.session.commit()
        return new_host, 201


@api.route('/<hostid>/<apikey>/')
@api.param('apikey', 'Your Api Key')
@api.param('hostid', 'Host id')
class HostResource(Resource):
    @api.doc('get_status_by_hostid')
    @api.marshal_with(stats_serializer)
    def get(self, hostid, apikey):
        owner = get_owner(ApiKey, apikey)
        hosts = [host.id for host in Hosts.query.filter_by(apikey_id=owner.id).all()]
        host_id = int(hostid) if int(hostid) in hosts else api.abort(403)
        stats = Stats.query.filter_by(host_id=host_id).all()
        return stats

    @api.doc('delete_host')
    @api.marshal_with(host_serializer, code=202)
    def delete(self, hostid, apikey):
        owner = get_owner(ApiKey, apikey)
        owned_hosts = [host.id for host in Hosts.query.filter_by(apikey_id=owner.id).all()]
        host_id = int(hostid) if int(hostid) in owned_hosts else api.abort(403)
        host_obj = Hosts.query.get(host_id)
        db.session.delete(host_obj)
        db.session.commit()
        return host_obj, 202


@api.route('/ping-task/', doc=False)
class HostResource(Resource):
    @api.doc('ping-task')
    def get(self):
        hosts = Hosts.query.filter_by(apikey_id=1).all()
        for _, host in enumerate(hosts):
            ping_host = requests.get(host.url, timeout=60)
            new_stat = Stats(
                code=ping_host.status_code,
                response_time=ping_host.elapsed.total_seconds()*1000,
                host_id=host.id,
            )
            db.session.add(new_stat)
            db.session.commit()
        return 'Ping task finished', 201


