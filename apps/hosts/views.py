import requests
from flask import request, abort
from flask_mail import Message
from flask_restx import Resource
from requests import exceptions
from apps.apikeys.models import ApiKey
from apps.apikeys.security import get_owner
from apps.extensions import mail
from apps.hosts.models import Hosts, Stats, db
from apps.hosts.namespace import (api,
                                  host_serializer,
                                  host_serializer_post,
                                  stats_serializer,
                                  host_serializer_mute)
from config import Settings
settings = Settings()

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
            return abort(400, 'This host does not seem to exist, please enter a valid http destination.')

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

    @api.doc('mute_by_hostid')
    @api.expect(host_serializer_mute)
    @api.marshal_with(host_serializer_mute, code=200)
    def put(self, hostid, apikey):
        owner = get_owner(ApiKey, apikey)
        hosts = [host.id for host in Hosts.query.filter_by(apikey_id=owner.id).all()]
        host_id = int(hostid) if int(hostid) in hosts else api.abort(403)
        host_obj = Hosts.query.get(host_id)
        host_obj.muted = request.json['muted']
        db.session.commit()
        return host_obj, 200

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
        hosts = Hosts.query.filter_by(muted=False).all()
        for _, host in enumerate(hosts):
            ping_host = {"status_code": 0,
                         "response_time": 0}

            try:
                ping_host_info = requests.get(host.url, timeout=60)
                ping_host['status_code'] = ping_host_info.status_code
                ping_host['response_time'] = int(ping_host_info.elapsed.total_seconds() * 1000)
            except exceptions.ConnectTimeout:
                ping_host['status_code'] = 408
                ping_host['response_time'] = 60000
            except exceptions.ConnectionError:
                ping_host['status_code'] = 404
                ping_host['response_time'] = 0

            new_stat = Stats(
                code=ping_host.get('status_code'),
                response_time=ping_host.get('response_time'),
                host_id=host.id,
            )
            if ping_host['status_code'] > 400:
                host_owner = ApiKey.query.get(host.apikey_id)
                message_body = f"Looks like there is a problem with the host you are monitoring. 🔔\n" \
                               f"Host name: {host.name}\n" \
                               f"Status code: {ping_host['status_code']}\n" \
                               f"Response time: {ping_host['response_time']} ms\n" \
                               f"Host url: {host.url}\n"

                if host_owner.chat_id is None:
                    msg = Message(f"Host monitor alert {host.name}",
                                  sender="host@monitor.com",
                                  recipients=[host_owner.email],
                                  body=message_body
                                  )
                    mail.send(msg)
                else:
                    body = {
                            "chat_id": host_owner.chat_id,
                            "host_id": host.id,
                            "text": message_body
                            }
                    requests.post(settings.BOT_NOTIFICATIONS_URL, json=body)

            db.session.add(new_stat)
            db.session.commit()
        return 'Ping task finished', 201
