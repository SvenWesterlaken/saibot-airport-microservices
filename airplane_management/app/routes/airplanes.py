from ..util.dto import AirplaneDto
from flask_restplus import Resource
from pony.orm import *
from ..util.rabbitmq_message import RabbitmqMessage
from ..rabbitmq import msg_publisher
from app.models import Airplane as f_airplane
import json
from flask import request

api = AirplaneDto.api
name = AirplaneDto.name
_airplane = AirplaneDto.airplane
publisher = msg_publisher.Message_publisher('events')


@api.route("/")
class Airplane_list(Resource):

    @db_session
    @api.doc('list_of_registered_airplanes')
    def get(self):
        airplanes = [f.to_dict() for f in f_airplane.select()]
        return json.dumps(airplanes)

    @db_session
    @api.doc('create new airplane')
    @api.expect(_airplane, validate=True)
    def post(self):
        airplane = request.json
        new_airplane = f_airplane(**airplane)

        message = RabbitmqMessage(message='New airplane has been added successfully', from_where=name,
                                  type=request.method, data=new_airplane.to_dict(),
                                  old_data='{}')

        publisher.publish_message(message.to_json(), api.name)

        return json.dumps(new_airplane.to_dict())

@api.route('/<public_id>')
@api.param('public_id', 'The Airplane identifier')
@api.response(404, 'Airplane not found.')
class Airplane(Resource):

    @db_session
    @api.doc('get an Airplane')
    def get(self, public_id):
        airplane = f_airplane[public_id]
        return json.dumps(airplane.to_dict())

    @db_session
    @api.doc('update an Airplane')
    @api.expect(_airplane)
    def put(self, public_id):
        airplane_update = request.json
        old_data = f_airplane[public_id].to_dict()
        airplane = f_airplane[public_id]
        airplane.update_props(airplane_update)

        message = RabbitmqMessage(message='Airplane has been updated successfully', from_where=name, type=request.method, data=airplane.to_dict(),
                                  old_data=old_data)

        publisher.publish_message(message.to_json(), api.name)

        return json.dumps(airplane.to_dict())

    @db_session
    @api.doc('delete an Airplane')
    def delete(self, public_id):
        airplane = f_airplane[public_id].to_dict()
        f_airplane[public_id].delete()

        message = RabbitmqMessage(message='Airplane has been deleted successfully', from_where=name, type=request.method,
                                  data="{}",
                                  old_data=airplane)

        publisher.publish_message(message.to_json(), api.name)
        return "success"








