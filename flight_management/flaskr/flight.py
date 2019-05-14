import json, arrow
from flask import Blueprint, request
from mongo import CheckInCounter, Flight, Gate

bp = Blueprint('flight', __name__, url_prefix='/flight')

@bp.route('/<id>/set_counter_gate', methods=['POST'])
def set_counter_and_gate(id):
    data = json.loads(request.data.decode('UTF-8'))
    counter = CheckInCounter(**data['counter'])
    gate = Gate(**data['gate'])

    flight = Flight.objects.get(id=id)
    flight.update_props({'check_in_counter': counter, 'gate': gate})
    flight.save()

    return json.dumps(flight.to_parsable())

@bp.route('/<id>/cancel', methods=['POST'])
def cancel_flight(id):
    flight = Flight.objects.get(id=id)
    flight.cancel()

    return json.dumps(flight.to_parsable())
