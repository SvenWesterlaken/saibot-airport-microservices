import functools, json, arrow
from flask import Blueprint, request
from models import CheckInCounter, Flight, Gate
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

@bp.route('/<id>/set_cg', methods=['PUT'])
@db_session
def set_counter_and_gate(id):
    data = json.loads(request.data.decode('UTF-8'))
    counter_id = data['check_in_counter']
    gate_id = data['gate']

    try:
        counter_id = int(counter_id)
    except ValueError:
        return 'Counter ID must be an integer', 400

    try:
        gate_id = int(gate_id)
    except ValueError:
        return 'Counter ID must be an integer', 400

    if CheckInCounter[counter_id] is None:
        return 'Invalid counter ID', 400

    if Gate[gate_id] is None:
        return 'Invalid gate ID', 400

    flight = Flight[id]
    flight.update_props({'check_in_counter': counter_id, 'gate': gate_id})

    return json.dumps(flight.to_dict())

@bp.route('/<id>/cancel', methods=['POST'])
@db_session
def cancel_flight(id):
    flight = Flight[id]
    flight.cancel()

    return json.dumps(flight.to_dict())
