import functools, json, arrow, uuid
from flask import Blueprint, request
from models import Gate
from pony.orm import *
from rabbitmq import msg_handler

bp = Blueprint('gate', __name__, url_prefix = '/gate')

@bp.route('', methods = ['GET'])
@db_session
def get_all():
    """
    Get all gates
    ---
    responses:
        200:
            description: Gates found
            schema:
                type: array
                items:
                    $ref: "#/definitions/Gate"
    """
    gates = [gate.to_dict() for gate in Gate.select()]

    return json.dumps(gates)

@bp.route('/<id>', methods = ['GET'])
@db_session
def get(id):
    """
    Get single gate by id
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the gate
    responses:
        200:
            description: Found a gate
            schema:
                $ref: "#/definitions/Gate"
        400:
            description: The given gate id is invalid
    """
    # Check if input is a number
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

@bp.route('', methods = ['POST'])
@db_session
def create():
    """
    Adds a gate to the system
    ---
    parameters:
        -   in: body
            name: gate
            description: The gate to create
            schema:
                type: object
                properties:
                    terminal:
                        type: string
                        description: Terminal of the gate
                        example: 'A'
                    number:
                        type: integer
                        description: Number of the gate
                        example: 1
    responses:
        200:
            description: Created a new gate
            schema:
                $ref: "#/definitions/Gate"
    """
    gate = json.loads(request.data.decode('UTF-8'))

    new_gate = Gate(**gate)

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'New gate has been added successfully',
        'from': 'gate_management',
        'type': 'CREATE',
        'data': new_gate.to_dict(),
        'old_data': {}
    }

    msg_handler.send_message_to_exchange('gate', json.dumps(payload))

    return json.dumps(new_gate.to_dict())

@bp.route('/<id>', methods = ['PUT'])
@db_session
def update(id):
    """
    Updates an existing gate in the system
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the gate
        -   in: body
            name: gate
            required: true
            schema:
                type: object
                properties:
                    terminal:
                        type: string
                        description: Terminal of the gate
                        example: 'A'
                    number:
                        type: integer
                        description: Number of the gate
                        example: 1
            description: The attributes of the gate to update
    responses:
        200:
            description: Updated the gate
            schema:
                $ref: "#/definitions/Gate"
        400:
            description: The given gate id is invalid
    """
    # Check if input is a number
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
    gate_old = gate.to_dict()  # Make dictionary of old gate object before updating it
    gate.update_props(gate_update)

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'Gate has been updated successfully',
        'from': 'game_management',
        'type': 'PUT',
        'data': gate.to_dict(),
        'old_data': gate_old
    }

    msg_handler.send_message_to_exchange('gate', json.dumps(payload))

    return json.dumps(gate.to_dict())

@bp.route('/<id>', methods = ['DELETE'])
@db_session
def delete(id):
    """
    Deletes an existing gate from the system
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the gate
    responses:
        200:
            description: Deleted the gate from the system
            schema:
                $ref: "#/definitions/Gate"
        400:
            description: The given gate id is invalid
    """
    # Check if input is a number
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
    gate_old = gate.to_dict()  # Make dictionary of old gate object before its deletion
    gate.delete()

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'Gate has been deleted successfully',
        'from': 'gate_management',
        'type': 'DELETE',
        'data': {},
        'old_data': gate_old
    }

    msg_handler.send_message_to_exchange('gate', json.dumps(payload))

    return 'Succeeded'
