from pony.orm import *
from .base import db, ParsingMixin
from datetime import datetime
import arrow

class Flight(db.Entity, ParsingMixin):
    nr = Required(int)
    type = Required(bool)
    location = Required(str)
    airline = Required('Airline')
    airplane = Required('Airplane')
    start_time = Optional(datetime, volatile=True)
    time = Required(datetime, volatile=True)
    end_time = Optional(datetime, volatile=True)
    status = Required(str, default='scheduled')
    check_in_counter = Optional('CheckInCounter')
    gate = Optional('Gate')
    updated_at = Required(datetime, default=arrow.now().datetime, volatile=True)
    created_at = Required(datetime, default=arrow.now().datetime, volatile=True)
    deleted_at = Optional(datetime, volatile=True)

    def cancel(self):
        self.status = 'canceled'
        deleted_at = arrow.now().datetime

    def set_before_and_after_time(self):
        time = arrow.get(self.time)
        is_departing = self.type

        self.start_time = time.shift(hours=-1).datetime if is_departing else time.shift(minutes=-15).datetime
        self.end_time = time.shift(minutes=+15).datetime if is_departing else time.shift(hours=+1).datetime

    def before_update(self):
        self.updated_at = arrow.now().datetime

    def before_insert(self):
        self.set_before_and_after_time()

    def to_dict(self, *args, **kwargs):
        dict = super().to_dict(*args, **kwargs)

        for k,v in dict.items():
            if isinstance(v, datetime):
                dict[k] = arrow.get(v).format('YYYY-MM-DD HH:mm:ss')

        return dict
