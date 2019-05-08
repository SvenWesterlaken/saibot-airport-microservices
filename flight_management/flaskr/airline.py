import functools, json
from flask import Blueprint, request
from models import Airline
from pony.orm import *

bp = Blueprint('airline', __name__, url_prefix='/airline')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    airlines = [airline.to_dict() for airline in Airline.select()]

    return json.dumps(airlines)

@bp.route('/<id>', methods=['GET'])
@db_session
def get(id):
    airline = Airline[id]
    return json.dumps(airline.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    airline = json.loads(request.data.decode('UTF-8'))
    new_airline = Airline(**airline)

    #TODO: Error Handling
    return json.dumps(new_airline.to_dict())

@bp.route('/<id>', methods=['PUT'])
@db_session
def update(id):
    airline_update = json.loads(request.data.decode('UTF-8'))
    airline = Airline[id]
    airline.update_props(airline_update)

    
    return json.dumps(airline.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    airline = Airline[id]

    airline.delete()

    #TODO: Error Handling
    return 'Succeeded'
