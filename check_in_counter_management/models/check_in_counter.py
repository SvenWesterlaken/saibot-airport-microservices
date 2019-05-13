from pony.orm import *
from .base import db, ParsingMixin

class CheckInCounter(db.Entity, ParsingMixin):
    _table_ = "check_in_counter"
    number = Required(int)
