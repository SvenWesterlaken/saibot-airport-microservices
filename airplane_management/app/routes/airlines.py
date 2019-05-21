from ..util.dto import AirlineDto
from flask_restplus import Resource
from pony.orm import *
from app.models import Airline as f_airline
import json
from flask import request
from ..util.rabbitmq_message import RabbitmqMessage
from ..rabbitmq import msg_publisher

api = AirlineDto.api
name = AirlineDto.name
_airline = AirlineDto.airline
publisher = msg_publisher.Message_publisher('events')


@api.route("/")
class Airline_list(Resource):

    @db_session
    @api.doc('list_of_registered_airlines')
    def get(self):
        airlines = [f.to_dict() for f in f_airline.select()]

        return json.dumps(airlines)

    @db_session
    @api.doc('create new airline')
    @api.expect(_airline, validate=True)
    def post(self):
        airline = request.json

        new_airline = f_airline(**airline)

        message = RabbitmqMessage(message='New airline has been added successfully', from_where=name, type=request.method, data=new_airline.to_dict(),
                                  old_data='{}')

        publisher.publish_message(message.to_json(), api.name)

        return json.dumps(new_airline.to_dict())


@api.route('/<public_id>')
@api.param('public_id', 'The Airline identifier')
@api.response(404, 'Airline not found.')
class Airline(Resource):

    @db_session
    @api.doc('get an Airline')
    def get(self, public_id):
        airline = f_airline[public_id]
        return json.dumps(airline.to_dict())

    @db_session
    @api.doc('update an Airline')
    @api.expect(_airline)
    def put(self, public_id):
        airline_update = request.json
        airline = f_airline[public_id]
        old_data = f_airline[public_id].to_dict()
        airline.update_props(airline_update)

        message = RabbitmqMessage(message='Airline has been updated successfully', from_where=name, type=request.method, data=airline.to_dict(),
                                  old_data=old_data)

        publisher.publish_message(message.to_json(), api.name)

        return json.dumps(airline.to_dict())

    @db_session
    @api.doc('delete an Airline')
    def delete(self, public_id):

        airline = f_airline[public_id].to_dict()
        f_airline[public_id].delete()

        message = RabbitmqMessage(message='Airline has been deleted successfully', from_where=name, type=request.method,
                                  data="{}",
                                  old_data=airline)

        publisher.publish_message(message.to_json(), api.name)

        return "success"


@api.route('/<public_id>/airplanes')
@api.param('public_id', 'The Airline identifier')
@api.response(404, 'Airline not found.')
class Airline_plane_list(Resource):
    @db_session
    @api.doc('list_of_registered_airplanes_connected_to_an_airline')
    def get(self, public_id):
        airplane_objcts = f_airline[public_id].airplanes
        airplanes = [x.to_dict() for x in airplane_objcts]
        return json.dumps(airplanes)
