from app.routes import bp
from ..util.dto import AirlineDto
from flask_restplus import Resource
from pony.orm import *
from app.models import Airline
import json

api = AirlineDto.api


@api.route("/")
@api.doc('list_of_registered_airlines')
class Airline_list(Resource):

    @db_session
    def get(self):
        airlines = [f.to_dict() for f in Airline.select()]
        return json.dumps(airlines)
