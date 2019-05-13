import functools, json, arrow
from flask import Blueprint, request
from models import Gate
from pony.orm import *

bp = Blueprint('gate', __name__, url_prefix='/gate')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    gates = [gate.to_dict() for gate in Gate.select()]

    return json.dumps(gates)

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

    # Check if gate with given id exists
    if Gate.get(id = id) is None:
        return 'Gate with id ' + id + ' does not exist', 400

    gate = Gate[id]

    return json.dumps(gate.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    gate = json.loads(request.data.decode('UTF-8'))

    new_gate = Gate(**gate)

    return json.dumps(new_gate.to_dict())

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

    # Check if gate with given id exists
    if Gate.get(id=id) is None:
        return 'Gate with id ' + id + ' does not exist', 400

    gate_update = json.loads(request.data.decode('UTF-8'))
    gate = Gate[id]
    gate.update_props(gate_update)

    return json.dumps(gate.to_dict())

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

    # Check if gate with given id exists
    if Gate.get(id=id) is None:
        return 'Gate with id ' + id + ' does not exist', 400

    gate = Gate[id]
    gate.delete()

    return 'Succeeded'
