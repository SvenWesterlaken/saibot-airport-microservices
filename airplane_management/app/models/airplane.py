from pony.orm import *
from .base import db, ParsingMixin

class Airplane(db.Entity, ParsingMixin):
    max_capacity = Required(int)
    airline = Required('Airline')
