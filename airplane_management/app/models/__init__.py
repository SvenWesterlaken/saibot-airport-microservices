import string
from random import randint
from pony.orm import db_session
from .base import db
from .airline import Airline
from .airplane import Airplane


@db_session
def populate_db():
    airlines = ['KLM', 'InterJet', 'Thomas Cook Airlines', 'Transavia Airlines', 'easyJet', 'Ryanair']
    airplanes = range(5)
    gate_terminals = string.ascii_uppercase[:2]
    gate_amount = range(10)
    airline_objects = []

    if not Airline.select().exists():
        for a in airlines:
            airline = Airline(name=a)
            airline_objects.append(airline)

    if not Airplane.select().exists():
        for i in airline_objects:
            for _ in airplanes:
                Airplane(max_capacity=randint(88, 268), airline=i)

