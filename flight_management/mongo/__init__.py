import arrow, mongoengine
from random import randint, choice
from .airplane import Airplane
from .check_in_counter import CheckInCounter
from .gate import Gate
from .baggage import Baggage
# Needs to be import after baggage (embedded document)
from .passenger import Passenger
# Needs to be last as embedded documents need to be imported first (registration of documents)
from .flight import Flight

def init(config, populate=True):
    connect_mongo(config)

    if not Flight.objects.count() > 0:
        populate_db()

def connect_mongo(config):
    print(' x', 'Connecting to mongodb...')
    mongoengine.connect(**config)
    print(' x', 'Connected to mongodb')

def populate_db():

    locations = ['Oakland, CA', 'Sacramento, CA', 'Seattle, WA', 'Las Vegas, NV', 'Phoenix, AZ']
    airlines = ['KLM', 'InterJet', 'Thomas Cook Airlines', 'Transavia Airlines', 'easyJet', 'Ryanair']

    for i in range(30):

        flight_props = {
            'nr': randint(50, 500),
            'type': randint(0,1) == 1,
            'location': choice(locations),
            'time': arrow.now().shift(days=i+1).replace(hour=randint(1,22), minute=randint(0,59), second=0, microsecond=0).datetime,
            'airplane': Airplane(e_id=randint(1,10), max_capacity=randint(88,268), airline=choice(airlines))
        }

        flight = Flight(**flight_props)
        flight.save()

    print(' x', 'Mongo Database populated')
