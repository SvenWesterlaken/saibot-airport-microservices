from pony.orm import *
from .base import db, ParsingMixin

class Airline(db.Entity, ParsingMixin):
    name = Required(str)
    flights = Set('Flight')
