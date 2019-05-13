from flask import Blueprint, request
from mongo import Flight
import json, arrow

bp = Blueprint('schedule', __name__, url_prefix='/schedule')

@bp.route('/<type>', methods=['GET'])
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

    flights = [f.to_json() for f in Flight.objects(time__gte=start_date.datetime, time__lte=end_date.datetime, type=type)]

    return json.dumps({'start': start_date.format('YYYY-MM-DD'), 'end': end_date.format('YYYY-MM-DD'), 'flights': flights})
#
# @bp.route('/request', methods=['POST'])
# @db_session
# def requestFreeGate():
#     flight = json.loads(request.data.decode('UTF-8'))
#
#     is_departing = flight['type'] == 1
#     time = arrow.get(flight['time'], 'YYYY-MM-DD HH:mm:ss')
#
#     flight['time'] = time.datetime
#     flight['type'] = is_departing
#
#     start_time = time.shift(hours=-1) if is_departing else time.shift(minutes=-15)
#     end_time = time.shift(minutes=+15) if is_departing else time.shift(hours=+1)
#
#     overlapping_count = select(f for f in Flight if f.start_time <= end_time.datetime and f.end_time >= start_time.datetime).count()
#     gates_count = Gate.select().count()
#
#     if overlapping_count < gates_count:
#         new_flight = Flight(**flight)
#
#         return json.dumps(new_flight.to_dict())
#     else:
#         return 'Sorry no free spots available around this time'
