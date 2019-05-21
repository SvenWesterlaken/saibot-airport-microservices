from mongoengine import *

airplane_schema = """
    properties:
        e_id:
            type: integer
            description: External ID of the airplane (from airplane_management)
        max_capacity:
            type: integer
            example: 88
            description: Max capacity for amount of passengers in the plane
        airline:
            type: string
            example: Transavia Airlines
            description: Airline owning this airplane
"""

class Airplane(EmbeddedDocument):
    e_id = IntField(required=True)
    max_capacity = IntField(required=True)
    airline = StringField(required=True)
