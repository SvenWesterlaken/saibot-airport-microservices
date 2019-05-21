import string, arrow
from random import randint, choice
from pony.orm import db_session
from .base import db
from .gate import *

schemas = [('Gate', gate_schema)]

@db_session
def populate_db():

    gate_terminals = string.ascii_uppercase[:2]
    gate_amount = range(10)

    if not Gate.select().exists():
        for t in gate_terminals:
            for number in gate_amount:
                Gate(terminal = t, number = number + 1)
