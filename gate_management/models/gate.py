from pony.orm import *
from .base import db, ParsingMixin

gate_schema = """
    properties:
        id:
            type: integer
            example: 2
            description: ID of the gate
        terminal:
            type: string
            example: 'A'
            description: Terminal of the gate
        number:
            type: integer
            example: 3
            description: Number of the gate
"""

class Gate(db.Entity, ParsingMixin):
    terminal = Required(str)
    number = Required(int)
