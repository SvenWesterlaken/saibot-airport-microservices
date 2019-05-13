from pony.orm import *
from .base import db, ParsingMixin


class Airline(db.Entity, ParsingMixin):
    name = Required(str)
    airplanes = Set('Airplane', cascade_delete=False)
