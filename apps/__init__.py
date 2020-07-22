from flask_restx import Api
from apps.apikeys.views import api as apikeys_namespace

# Swagger API
api = Api(title='Host Monitor API', version='1.0.0',
          description='Host Monitor API',
          )

api.add_namespace(apikeys_namespace)
