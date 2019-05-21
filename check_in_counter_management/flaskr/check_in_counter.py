import functools, json, arrow, uuid
from flask import Blueprint, request
from models import CheckInCounter
from pony.orm import *
from rabbitmq import msg_handler

bp = Blueprint('check_in_counter', __name__, url_prefix='/checkincounter')

@bp.route('', methods=['GET'])
@db_session
def get_all():
    """
    Get all check-in counters
    ---
    responses:
        200:
            description: Check-in counters found
            schema:
                type: array
                items:
                    $ref: "#/definitions/CheckInCounter"
    """
    counters = [counter.to_dict() for counter in CheckInCounter.select()]

    return json.dumps(counters)

@bp.route('/<id>', methods=['GET'])
@db_session
def get(id):
    """
    Get single check-in counter by id
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the check-in counter
    responses:
        200:
            description: Found a check-in counter
            schema:
                $ref: "#/definitions/CheckInCounter"
        400:
            description: The given counter id is invalid
    """
    # Check if input is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"', 400

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"', 400

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id = id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter = CheckInCounter[id]

    return json.dumps(counter.to_dict())

@bp.route('', methods=['POST'])
@db_session
def create():
    """
    Adds a check-in counter to the system
    ---
    parameters:
        -   in: body
            name: counter
            description: The check-in counter to create
            schema:
                type: object
                properties:
                    number:
                        type: integer
                        description: Number of the check-in counter
                        example: 4
    responses:
        200:
            description: Created a new check-in counter
            schema:
                $ref: "#/definitions/CheckInCounter"
    """
    counter = json.loads(request.data.decode('UTF-8'))

    new_counter = CheckInCounter(**counter)

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'New check-in counter has been added successfully',
        'from': 'check_in_counter_management',
        'type': 'CREATE',
        'data': new_counter.to_dict(),
        'old_data': {}
    }

    msg_handler.send_message_to_exchange('check-in-counter', json.dumps(payload))

    return json.dumps(new_counter.to_dict())

@bp.route('/<id>', methods=['PUT'])
@db_session
def update(id):
    """
    Updates an existing check-in counter in the system
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the check-in counter
        -   in: body
            name: counter
            required: true
            schema:
                type: object
                properties:
                    number:
                        type: integer
                        description: Number of the check-in counter
                        example: 4
            description: The attributes of the check-in counter to update
    responses:
        200:
            description: Updated the check-in counter
            schema:
                $ref: "#/definitions/CheckInCounter"
        400:
            description: The given counter id is invalid

    """
    # Check if input is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"', 400

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"', 400

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id=id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter_update = json.loads(request.data.decode('UTF-8'))
    counter = CheckInCounter[id]
    counter_old = counter.to_dict() # Make dictionary of old counter object before updating it
    counter.update_props(counter_update)

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'Check-in counter has been updated successfully',
        'from': 'check_in_counter_management',
        'type': 'PUT',
        'data': counter.to_dict(),
        'old_data': counter_old
    }

    msg_handler.send_message_to_exchange('check-in-counter', json.dumps(payload))

    return json.dumps(counter.to_dict())

@bp.route('/<id>', methods=['DELETE'])
@db_session
def delete(id):
    """
    Deletes an existing check-in counter from the system
    ---
    parameters:
        -   in: path
            name: id
            required: true
            schema:
                type: number
                example: 1
            description: ID of the check-in counter
    responses:
        200:
            description: Deleted the check-in counter from the system
            schema:
                $ref: "#/definitions/CheckInCounter"
        400:
            description: The given counter id is invalid
    """
    # Check if input is a number
    try:
        int(id)
    except ValueError:
        return 'Invalid id \"' + id + '\"', 400

    # Check if input number is smaller than 32 bit int
    if not abs(int(id)) <= 0xffffffff:
        return 'Invalid id \"' + id + '\"', 400

    # Check if check-in counter with given id exists
    if CheckInCounter.get(id=id) is None:
        return 'Check-in counter with id ' + id + ' does not exist', 400

    counter = CheckInCounter[id]
    counter_old = counter.to_dict() # Make dictionary of old counter object before its deletion
    counter.delete()

    payload = {
        'id': str(uuid.uuid4()),
        'message': 'Check-in counter has been deleted successfully',
        'from': 'check_in_counter_management',
        'type': 'DELETE',
        'data': {},
        'old_data': counter_old
    }

    msg_handler.send_message_to_exchange('check-in-counter', json.dumps(payload))

    return 'Succeeded'
