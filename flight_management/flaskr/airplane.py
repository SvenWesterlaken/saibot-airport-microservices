import functools, json
from flask import Blueprint, request
from models import Airplane
from pony.orm import *

bp = Blueprint('airplane', __name__, url_prefix='/airplane')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    airlines = [airplane.to_dict() for airplane in Airplane.select()]

    return json.dumps(airlines)

@bp.route('/<id>', methods=['GET'])
@db_session
def get(id):
    airplane = Airplane[id]
    return json.dumps(airplane.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    airplane = json.loads(request.data.decode('UTF-8'))
    new_airline = Airplane(**airplane)

    #TODO: Error Handling
    return json.dumps(new_airline.to_dict())

@bp.route('/<id>', methods=['PUT'])
@db_session
def update(id):
    airplane_update = json.loads(request.data.decode('UTF-8'))
    airplane = Airplane[id]
    airline.update_props(airplane_update)


    return json.dumps(airline.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    airplane = Airplane[id]

    airplane.delete()

    #TODO: Error Handling
    return 'Succeeded'
