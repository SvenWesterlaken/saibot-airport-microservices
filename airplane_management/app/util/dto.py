from flask_restplus import Namespace, fields


class AirlineDto:
    api = Namespace('airline', description='airline related operations')
    airline = api.model('airline', {
        'name': fields.String(required=True, description='name of airline'),
    })
    name = 'airplane_management'

class AirplaneDto:
    api = Namespace('airplane', description='airplane related operations')
    airplane = api.model('airplane', {
        'max_capacity': fields.Integer(required=True, description='Maximum capacity for airplane to hold passengers'),
        'airline': fields.Integer(required=True, description='Foreign key of airline')
    })
    name = "airplane_management"
