from app.routes import bp
from ..util.dto import AirlineDto
from flask_restplus import Resource
from pony.orm import *
from app.models import Airline as f_airline
from app.models import Airplane as f_airplane
import json
from flask import request

api = AirlineDto.api
_airline = AirlineDto.airline


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
        airline.update_props(airline_update)

        return json.dumps(airline.to_dict())

    @db_session
    @api.doc('delete an Airline')
    def delete(self, public_id):
        f_airline[public_id].delete()
        return "success"


@api.route('/<public_id>/airplanes')
@api.param('public_id', 'The Airline identifier')
@api.response(404, 'Airline not found.')
class Airline_plane_list(Resource):
    @db_session
    @api.doc('list_of_registered_airplanes_connected_to_an_airline')
    def get(self, public_id):
        airplanes = f_airline[public_id].airplanes
        return json.dumps(airplanes)










