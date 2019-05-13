import functools, json, arrow
from flask import Blueprint, request
from models import CheckInCounter
from pony.orm import *

bp = Blueprint('check_in_counter', __name__, url_prefix='/checkincounter')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    counters = [counter.to_dict() for counter in CheckInCounter.select()]

    return json.dumps(counters)

@bp.route('/<id>', methods=['GET'])
@db_session
def get(id):
    # Check if input it is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"'

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"'

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id = id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter = CheckInCounter[id]

    return json.dumps(counter.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    counter = json.loads(request.data.decode('UTF-8'))

    new_counter = CheckInCounter(**counter)

    return json.dumps(new_counter.to_dict())

@bp.route('/<id>', methods=['PUT'])
@db_session
def update(id):
    # Check if input it is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"'

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"'

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id=id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter_update = json.loads(request.data.decode('UTF-8'))
    counter = CheckInCounter[id]
    counter.update_props(counter_update)

    return json.dumps(counter.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    # Check if input it is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"'

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"'

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id=id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter = CheckInCounter[id]
    counter.delete()

    return 'Succeeded'
