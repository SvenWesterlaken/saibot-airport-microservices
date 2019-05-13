from flask import Blueprint
from flask_restplus import Api
from app.routes.airlines import api as airline_ns


# from .apis.namespace1 import api as ns1
# from .apis.namespace2 import api as ns2
# # ...
# from .apis.namespaceX import api as nsX

blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(blueprint,
    title='My Title',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(airline_ns)

