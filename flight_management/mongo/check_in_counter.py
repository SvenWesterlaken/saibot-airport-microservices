from mongoengine import *

counter_schema = """
    properties:
        e_id:
            type: integer
            example: 2
            description: External ID of the check-in counter (from check_in_counter_management)
        nr:
            type: integer
            example: 2
            description: Number of the check-in counter
"""

class CheckInCounter(EmbeddedDocument):
    e_id = IntField(required=True)
    nr = IntField(required=True)
