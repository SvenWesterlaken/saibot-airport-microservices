import string
from random import randint
from pony.orm import db_session
from .base import db
from .flight import Flight
from .airline import Airline
from .airplane import Airplane
from .gate import Gate

@db_session
def populate_db():

    if not Airline.select().exists():
        airlines = ['KLM', 'InterJet', 'Thomas Cook Airlines', 'Transavia Airlines', 'easyJet', 'Ryanair']

        for a in airlines:
            Airline(name=a)

    if not Airplane.select().exists():

        for i in range(10):
            Airplane(max_capacity=randint(88, 268))

    if not Gate.select().exists():
        for t in string.ascii_uppercase[:2]:
            for nr in range(10):
                Gate(terminal=t, nr=nr+1)


    if not Flight.select().exists():
        pass
