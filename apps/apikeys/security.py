import hashlib
import os


def encrypt(apikey):
    salt = os.getenv('SALT')
    return hashlib.sha512((apikey + salt).encode('utf-8')).hexdigest()


def verify_apikey(apikey_hash, apikey):
    if apikey_hash != encrypt(apikey):
        return False
    else:
        return True
