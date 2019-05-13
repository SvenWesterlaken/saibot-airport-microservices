import arrow, mongoengine
from random import randint, choice
from .flight import Flight
# from .base import db
# from .flight import Flight
# from .airline import Airline
# from .airplane import Airplane
# from .cargo import Cargo
# from .check_in_counter import CheckInCounter
# from .gate import Gate
# from .passenger import Passenger

def init(config, populate=True):
    connect_mongo(config)
    populate_db()


def connect_mongo(config):
    print(' x', 'Connecting to mongodb...')
    mongoengine.connect(**config)
    print(' x', 'Connected to mongodb')

def populate_db():

    locations = ['Oakland, CA', 'Sacramento, CA', 'Seattle, WA', 'Las Vegas, NV', 'Phoenix, AZ']
    airlines = ['KLM', 'InterJet', 'Thomas Cook Airlines', 'Transavia Airlines', 'easyJet', 'Ryanair']

    if Flight.objects.count() == 0:
        for i in range(30):

            flight_props = {
                'nr': randint(50, 500),
                'type': randint(0,1) == 1,
                'location': choice(locations),
                'time': arrow.now().shift(days=i+1).replace(hour=randint(1,22), minute=randint(0,59)).ceil('minute').datetime
            }

            flight = Flight(**flight_props)
            flight.save()
