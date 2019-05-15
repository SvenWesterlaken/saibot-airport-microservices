import json, arrow
from flask import Blueprint, request
from mongo import CheckInCounter, Flight, Gate, Passenger

bp = Blueprint('flight', __name__, url_prefix='/flight')

@bp.route('/<id>', methods=['GET'])
def get_flight(id):
    flight = Flight.objects.get(id=id)

    return json.dumps(flight.to_parsable())

@bp.route('', methods=['GET'])
def get_all():
    flights = [f.to_parsable() for f in Flight.objects]
    return json.dumps(flights)

@bp.route('/count', methods=['GET'])
def get_count():
    return json.dumps({'count': Flight.objects.count()})

@bp.route('/schedule/<type>', methods=['GET'])
def getSchedule(type):
    params = request.args

    now = arrow.now().date()
    type = bool(int(type))

    start_date = arrow.get(now)
    end_date = arrow.get(now).shift(days=+1)

    if 'start_date' in params.keys():
        start_date = arrow.get(params['start_date'])

    if 'end_date' in params.keys():
        end_date = arrow.get(params['end_date'])

    flights = [f.to_parsable() for f in Flight.objects(time__gte=start_date.datetime, time__lte=end_date.datetime, type=type)]

    return json.dumps({'start': start_date.format('YYYY-MM-DD'), 'end': end_date.format('YYYY-MM-DD'), 'flights': flights})

@bp.route('/request', methods=['POST'])
def requestFreeGate():
    flight = json.loads(request.data.decode('UTF-8'))

    is_departing = flight['type'] == 1
    time = arrow.get(flight['time'], 'YYYY-MM-DD HH:mm:ss')

    flight['time'] = time.datetime
    flight['type'] = is_departing

    start_time = time.shift(hours=-1) if is_departing else time.shift(minutes=-15)
    end_time = time.shift(minutes=+15) if is_departing else time.shift(hours=+1)

    overlapping_count = Flight.objects(start_time__lte=end_time.datetime, time__gte=start_time.datetime).count()
    gates_count = 20 # needs to be coupled to a database value

    if overlapping_count < gates_count:
        new_flight = Flight(**flight)
        new_flight.save()

        return json.dumps(new_flight.to_parsable())
    else:
        return 'Sorry no free spots available around this time'

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

@bp.route('/<id>/add_passenger', methods=['POST'])
def add_passenger(id):
    flight = Flight.objects.get(id=id)

    passengers = json.loads(request.data.decode('UTF-8'))

    if isinstance(passengers, dict):
        passengers = [passengers]

    for p in passengers:
        flight.passengers.append(Passenger(**p))

    flight.save()

    return json.dumps(flight.to_parsable())
