import string, arrow
from random import randint, choice
from pony.orm import db_session
from .base import db
from .check_in_counter import *

schemas = [('CheckInCounter', counter_schema)]

@db_session
def populate_db():

    check_in_counter_amount = range(10)

    if not CheckInCounter.select().exists():
        for number in check_in_counter_amount:
            CheckInCounter(number = number + 1)
