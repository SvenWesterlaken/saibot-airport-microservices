from flask import Blueprint, request, render_template
from pony.orm import *
from models import Flight, Gate
import json, arrow

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/<type>', methods=['GET'])
@db_session
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

    flights = [f.to_dict() for f in select(f for f in Flight if f.time >= start_date.datetime and f.time <= end_date.datetime and f.type == type)[:]]

    return json.dumps({'start': start_date.format('YYYY-MM-DD'), 'end': end_date.format('YYYY-MM-DD'), 'flights': flights})

@bp.route('/request', methods=['POST'])
@db_session
def requestFreeGate():
    flight = json.loads(request.data.decode('UTF-8'))

    is_departing = flight['type'] == 1
    time = arrow.get(flight['time'], 'YYYY-MM-DD HH:mm:ss')

    flight['time'] = time.datetime
    flight['type'] = is_departing

    start_time = time.shift(hours=-1) if is_departing else time.shift(minutes=-15)
    end_time = time.shift(minutes=+15) if is_departing else time.shift(hours=+1)

    overlapping_count = select(f for f in Flight if f.start_time <= end_time.datetime and f.end_time >= start_time.datetime).count()
    gates_count = Gate.select().count()

    if overlapping_count < gates_count:
        new_flight = Flight(**flight)
        commit()

        print(new_flight.start_time)

        return json.dumps(new_flight.to_dict())
    else:
        return 'Sorry no free spots available'
