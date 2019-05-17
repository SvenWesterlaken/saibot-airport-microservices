from app.routes import bp
from ..util.dto import AirlineDto, AirplaneDto
from flask_restplus import Resource
from pony.orm import *
from app.models import Airline as f_airline
from app.models import Airplane as f_airplane
import json
from flask import request

api = AirplaneDto.api
_airplane = AirplaneDto.airplane


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
        airplane = f_airplane[public_id]
        airplane.update_props(airplane_update)

        return json.dumps(airplane.to_dict())

    @db_session
    @api.doc('delete an Airplane')
    def delete(self, public_id):
        f_airplane[public_id].delete()
        return "success"








