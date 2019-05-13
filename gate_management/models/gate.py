from pony.orm import *
from .base import db, ParsingMixin

class Gate(db.Entity, ParsingMixin):
    terminal = Required(str)
    number = Required(int)
