from pony.orm import *
from .base import db, ParsingMixin

class Passenger(db.Entity, ParsingMixin):
    last_name = Required(str)
