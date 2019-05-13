from flask import Blueprint
from flask_restplus import Api
from app.routes.airlines import api as airline_ns
from app.routes.airplanes import api as airplane_ns
from pony.orm import *

blueprint = Blueprint('api', __name__, url_prefix='/api/1')
api = Api(blueprint,
    title='My Title',
    version='1.0',
    description='A description',
    doc='/docs'
    # All API metadatas
)

api.add_namespace(airline_ns)
api.add_namespace(airplane_ns)

@api.errorhandler(ObjectNotFound)
def handle_root_exception(error):
    '''Return a custom message and 400 status code'''
    return {'message': 'Object was not found'}, 404


@api.errorhandler(ConstraintError)
def handle_custom_exception(error):
    '''Return a custom message and 404 status code'''
    return {'message': 'Cannot delete object that has child objects'}, 400


