from pony.orm import *
from .base import db
from datetime import datetime
import arrow

class Flight(db.Entity):
    nr = Required(int)
    from_location = Required(str)
    to_location = Required(str)
    airline = Required('Airline')
    status = Required(str, default='scheduled')
    take_off_time = Required(datetime)
    arrival_time = Required(datetime)
    leave_gate = Required('Gate', reverse='leaving_flights')
    arrival_gate = Required('Gate', reverse='arrival_flights')
    updated_at = Required(datetime, default=arrow.now().datetime)
    created_at = Required(datetime, default=arrow.now().datetime)

    def before_update(self):
        self.updated_at = arrow.now().datetime
