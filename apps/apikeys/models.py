from config import db, ma
from apps.apikeys.security import verify_apikey


class ApiKey(db.Model):
    __tablename__ = 'apikeys'
    id = db.Column(db.Integer, primary_key=True)
    apikey = db.Column(db.String, unique=True, nullable=False)
    apikey_hash = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)

    def check_apikey(self, apikey):
        return verify_apikey(apikey_hash=self.apikey_hash, apikey=apikey)

    def __init__(self, apikey, apikey_hash, email):
        self.apikey = apikey
        self.apikey_hash = apikey_hash
        self.email = email


class ApiKeySchema(ma.Schema):
    class Meta:
        fields = ('id', 'apikey', 'apikey_hash', 'email')


apikey_schema = ApiKeySchema()
apikeys_schema = ApiKeySchema(many=True)
