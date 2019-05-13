import string, arrow
from random import randint, choice
from pony.orm import db_session
from .base import db
from .flight import Flight
from .airline import Airline
from .airplane import Airplane
from .cargo import Cargo
from .check_in_counter import CheckInCounter
from .gate import Gate
from .passenger import Passenger

@db_session
def populate_db():

    airlines = ['KLM', 'InterJet', 'Thomas Cook Airlines', 'Transavia Airlines', 'easyJet', 'Ryanair']
    airplanes = range(10)
    cargo = range(10)
    check_in_counters = range(10)
    gate_terminals = string.ascii_uppercase[:2]
    gate_amount = range(10)
    passengers = ['Henderson', 'Brewster', 'Wilson']

    if not Airline.select().exists():
        for a in airlines:
            airline = Airline(name=a)

    if not Airplane.select().exists():
        for i in airplanes:
            Airplane(max_capacity=randint(88, 268))

    if not Cargo.select().exists():
        for c in cargo:
            Cargo(weight=randint(0, 10000))

    if not CheckInCounter.select().exists():
        for c in check_in_counters:
            CheckInCounter(nr=c+1)

    if not Gate.select().exists():
        for t in gate_terminals:
            for nr in gate_amount:
                Gate(terminal=t, nr=nr+1)


    if not Flight.select().exists():
        now = arrow.now()
        locations = ['Oakland, CA', 'Sacramento, CA', 'Seattle, WA', 'Las Vegas, NV', 'Phoenix, AZ']

        for i in range(1,31):

            flight_props = {
                'nr': randint(50,500),
                'type': randint(0,1) == 1,
                'location': choice(locations),
                'airline': randint(1, len(airlines)),
                'airplane': randint(1, len(airplanes)),
                'time': now.shift(days=+i).replace(hour=randint(1,22), minute=randint(0,59), second=0).datetime,
                'check_in_counter': randint(1, len(check_in_counters)),
                'gate': randint(1, len(gate_terminals) * len(gate_amount))
            }

            Flight(**flight_props)

    if not Passenger.select().exists():
        for p in passengers:
            Passenger(last_name=p)
