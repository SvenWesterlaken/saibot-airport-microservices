from flask_restplus import Namespace, fields


class AirlineDto:
    api = Namespace('airline', description='user related operations')
    user = api.model('airline', {
        'name': fields.String(required=True, description='name of airline'),
    })