import hashlib
import os
import uuid


def gen_new_key():
    return str(uuid.uuid4())


def encrypt(apikey):
    salt = os.getenv('SALT')
    return hashlib.sha512((apikey + salt).encode('utf-8')).hexdigest()


def verify_apikey(api, apikey_hash, apikey):
    if apikey_hash != encrypt(apikey):
        return api.abort(403)
    else:
        return True


def get_owner(obj, apikey):
    query = obj.query.filter_by(apikey_hash=encrypt(apikey)).first_or_404()
    return query
