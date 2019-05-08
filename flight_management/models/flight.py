from pony.orm import *
from .base import db

class Flight(db.Entity):
    nr = Required(int)
