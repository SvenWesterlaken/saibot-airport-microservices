from app.routes import bp
from ..util.dto import AirlineDto
from flask_restplus import Resource
from pony.orm import *
from app.models import Airline
import json
from flask import request

api = AirlineDto.api
_airline = AirlineDto.user


@api.route("/")
class Airline_list(Resource):

    @db_session
    @api.doc('list_of_registered_airlines')
    def get(self):
        airlines = [f.to_dict() for f in Airline.select()]
        return json.dumps(airlines)

    @db_session
    @api.doc('create new airline')
    @api.expect(_airline, validate=True)
    def post(self):
        airline = request.json
        new_airline = Airline(**airline)
        return json.dumps(new_airline)

@api.route('/<public_id>')
@api.param('public_id', 'The Airline identifier')
@api.response(404, 'Airline not found.')
class Airline(Resource):

    @db_session
    @api.doc('get an Airline')
    def get(self, public_id):
        try:
            flight = Airline[public_id]
            return json.dumps(flight.to_dict())
        except ObjectNotFound:
            api.abort(404)

    @db_session
    @api.doc('update an Airline')
    def put(self, public_id):
        airplane_update = request.json
        airplane = Airline[public_id]
        airplane.update_props(airplane_update)

        return json.dumps(airplane.to_dict())

    @db_session
    @api.doc('delete an Airline')
    def delete(self, public_id):
        flight = None
        try:
            flight = Airline[public_id]
        except ObjectNotFound:
            api.abort(404)

        try:
            flight[public_id].delete()
        except ConstraintError:
            api.abort(400, "Airline still has airplanes")
        return json.dumps(flight.to_dict())








