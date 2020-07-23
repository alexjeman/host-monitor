from config.settings import Settings
ma = Settings.ma


class HostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'url')


host_schema = HostSchema()
hosts_schema = HostSchema(many=True)


class StatsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ping', 'time')


stat_schema = StatsSchema()
stats_schema = StatsSchema(many=True)
