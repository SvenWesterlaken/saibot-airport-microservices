from db import r as redis
from flask import Blueprint, request, jsonify
import json, arrow

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('', methods=['GET'])
@bp.route('/<ns>', methods=['GET'])
def get_events(ns='events'):
    """
    get events (or logs) with given filters
    ---
    tags:
        -   events & logs
    definitions:
        - schema:
            id: 'Event'
            properties:
                ts:
                    type: string
                    example: '2019-05-21 12:21:56'
                    description: timestamp of the event
                event:
                    type: object
                    description: information contained by the event
                    properties:
                        from:
                            type: string
                            example: 'flight_management'
                            description: name of microservice where the event came from
                        id:
                            type: string
                            format: uuid
                            example: f3cc71f10cbe42e6b7902052150db7d4
                            description: UUID of the event
                        message:
                            type: string
                            example: New flight has been added successfully.
                            description: Informative message for the event
                        type:
                            type: string
                            example: CREATE
                            description: Type of event
                        data:
                            type: object
                            description: 'Newly created or updated data'
                            properties:
                        old_data:
                            type: object
                            properties:
                            description: 'Old data (incase of an update or deletion)'

        - schema:
            id: 'Log'
            type: string
            example: '[2019-05-21 12:21:56] New flight has been added successfully.'
    parameters:
        -   in: path
            name: ns
            required: false
            schema:
                type: string
                example: flight
            description: 'namespace for events (first part of the event topic, ie. flight.create = **flight**)'
        -   in: query
            name: min_date
            schema:
                type: string
                example: '2019-05-15 12:00:00'
            description: 'Timestamp from where to start the logs'
        -   in: query
            name: max_date
            schema:
                type: string
                example: '2019-05-15 12:30:00'
            description: Timestamp from where to end the logs
        -   in: query
            name: logs
            schema:
                type: boolean
            description: 'Whether to get logs (**true**) json objects of events (**false**)'
        -   in: query
            name: desc
            schema:
                type: boolean
            description: 'Whether to display the items in descending order or not'

    responses:
        200:
            description: Events data (if logs not set to true)
            schema:
                $ref: '#/definitions/Event'
        404:
            description: 'No events found (for given criteria)'
            schema:
                type: object
                properties:
                    msg:
                        type: string
                        example: no events found
    """

    events, is_logs = redis.get_events(ns, **request.args)

    if len(events) > 0:
        return '\n'.join(events) if is_logs else jsonify(events)

    return jsonify({'msg': 'no events found'}), 404
