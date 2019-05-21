from mongoengine import *

baggage_schema = """
    properties:
        weight:
            type: integer
            example: 25
            description: Weight of the baggage in kilograms
"""

class Baggage(EmbeddedDocument):
    weight = IntField(required=True, default=0)
