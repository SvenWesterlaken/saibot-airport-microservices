from pony.orm import *
from .base import db, ParsingMixin

counter_schema = """
    properties:
        id:
            type: integer
            example: 2
            description: ID of the check-in counter
        number:
            type: integer
            example: 3
            description: Number of the check-in counter
"""

class CheckInCounter(db.Entity, ParsingMixin):
    _table_ = "check_in_counter"
    number = Required(int)
