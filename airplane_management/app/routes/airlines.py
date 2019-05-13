from app.routes import bp
from ..util.dto import AirlineDto
from flask_restplus import Resource

api = AirlineDto.api

@api.route("/")
@api.doc('list_of_registered_airlines')
class Airline_list(Resource):
    def get(self):
        return "Hello World!"
