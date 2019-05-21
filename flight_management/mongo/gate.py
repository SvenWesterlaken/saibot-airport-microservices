from mongoengine import *

gate_schema = """
    properties:
        e_id:
            type: integer
            example: 2
            description: External ID of the gate (from gate_management)
        terminal:
            type: string
            example: A
            description: Terminal (consisting of one letter)
        nr:
            type: integer
            example: 2
            description: Number of the gate
"""

class Gate(EmbeddedDocument):
    e_id = IntField(required=True)
    terminal = StringField(max_length=1, required=True)
    nr = IntField(required=True)
