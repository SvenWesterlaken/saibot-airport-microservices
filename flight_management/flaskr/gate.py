import functools, json
from flask import Blueprint, request
from models import db, Gate
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
    gate_update = json.loads(request.data.decode('UTF-8'))
    gate = Gate[id]
    gate.update_props(gate_update)

    return json.dumps(gate.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    gate = Gate[id]

    gate.delete()

    return 'Succeeded'
