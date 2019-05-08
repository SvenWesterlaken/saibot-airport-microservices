from pony.orm import *
from .base import db

class Gate(db.Entity):
    terminal = Required(str)
    nr = Required(int)
    arrival_flights = Set('Flight', reverse='arrival_gate')
    leaving_flights = Set('Flight', reverse='leave_gate')
