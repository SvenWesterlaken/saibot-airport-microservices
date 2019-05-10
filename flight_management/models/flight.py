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
    time = Required(datetime)
    status = Required(str, default='scheduled')
    check_in_counter = Optional('CheckInCounter')
    gate = Optional('Gate')
    updated_at = Required(datetime, default=arrow.now().datetime)
    created_at = Required(datetime, default=arrow.now().datetime)

    def before_update(self):
        self.updated_at = arrow.now().datetime

    def to_dict(self, *args, **kwargs):
        dict = super().to_dict(*args, **kwargs)

        for k,v in dict.items():
            if isinstance(v, datetime):
                dict[k] = arrow.get(v).format('YYYY-MM-DD HH:mm:ss')

        return dict
