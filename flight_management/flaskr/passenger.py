# import functools, json, arrow
# from flask import Blueprint, request
# from models import Passenger
# from pony.orm import *
#
# bp = Blueprint('passenger', __name__, url_prefix='/passenger')
#
# @bp.route('', methods=['GET'])
# @db_session
# def get_all():
#     passengers = [p.to_dict() for p in Passenger.select()]
#
#     return json.dumps(passengers)
#
# @bp.route('/<id>', methods=['GET'])
# @db_session
# def get(id):
#     passenger = Passenger[id]
#
#     return json.dumps(passenger.to_dict())
#
# @bp.route('', methods=['POST'])
# @db_session
# def create():
#     passenger = json.loads(request.data.decode('UTF-8'))
#
#     new_passenger = Passenger(**passenger)
#
#     return json.dumps(new_passenger.to_dict())
#
# @bp.route('/<id>', methods=['PUT'])
# @db_session
# def update(id):
#     passenger_update = json.loads(request.data.decode('UTF-8'))
#     passenger = Passenger[id]
#     passenger.update_props(passenger_update)
#
#     return json.dumps(passenger.to_dict())
#
# @bp.route('/<id>', methods=['DELETE'])
# @db_session
# def delete(id):
#     passenger = Passenger[id]
#
#     passenger.delete()
#
#     return 'Succeeded'
