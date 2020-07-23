from config.settings import Settings

ma = Settings.ma


class ApiKeySchema(ma.Schema):
    class Meta:
        fields = ('id', 'apikey', 'apikey_hash', 'email')


apikey_schema = ApiKeySchema()
apikeys_schema = ApiKeySchema(many=True)
