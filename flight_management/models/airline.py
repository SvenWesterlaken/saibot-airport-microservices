from pony.orm import *
from .base import db

class Airline(db.Entity):
    name = Required(str)
    flights = Set('Flight')
