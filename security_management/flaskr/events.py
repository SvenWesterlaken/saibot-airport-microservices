from db import r as redis
from flask import Blueprint, request, jsonify
import json, arrow

bp = Blueprint('events', __name__, url_prefix='/events')

@bp.route('', methods=['GET'])
@bp.route('/', methods=['GET'])
@bp.route('/<ns>', methods=['GET'])
def get_events(ns='events'):

    events, is_logs = redis.get_events(ns, **request.args)

    if len(events) > 0:
        return '\n'.join(events) if is_logs else jsonify(events)

    return jsonify({'msg': 'no events found'}), 404
