import functools, json, arrow
from flask import Blueprint, request
from models import CheckInCounter, Flight
from pony.orm import *

bp = Blueprint('flight', __name__, url_prefix='/flight')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    flights = [f.to_dict() for f in Flight.select()]

    return json.dumps(flights)

@bp.route('/<id>', methods=['GET'])
@db_session
def get(id):
    flight = Flight[id]
    return json.dumps(flight.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    flight = json.loads(request.data.decode('UTF-8'))
    flight['time'] = arrow.get(flight['time'], 'YYYY-MM-DD HH:mm:ss').datetime

    new_flight = Flight(**flight)

    return json.dumps(new_flight.to_dict())

@bp.route('/<id>', methods=['PUT'])
@db_session
def update(id):
    flight_update = json.loads(request.data.decode('UTF-8'))
    flight = Flight[id]
    flight.update_props(flight_update)

    return json.dumps(flight.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    flight = Flight[id]

    flight.delete()

    #TODO: Error Handling
    return 'Succeeded'

@bp.route('/<id>/setcounter', methods=['PUT'])
@db_session
def set_counter(id):
    flight_data = json.loads(request.data.decode('UTF-8'))
    counter_id = flight_data['check_in_counter']

    try:
        int(counter_id)
    except ValueError:
        return 'Counter id must be an integer', 400

    if CheckInCounter.get(id=counter_id) is None:
        return 'Invalid counter id', 400

    flight = Flight[id]

    setattr(flight, 'check_in_counter', counter_id)

    return json.dumps(flight.to_dict())