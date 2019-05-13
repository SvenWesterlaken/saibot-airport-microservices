from mongoengine import *
import arrow

STATUS_SCHEDULED = 0
STATUS_CANCELED = 1
STATUS_ARRIVED = 2
STATUS_DEPARTED = 3

class Flight(Document):
    nr = IntField(required=True)
    type = BooleanField()
    location = StringField()
    start_time = DateTimeField()
    time = DateTimeField()
    end_time = DateTimeField()
    status = IntField(default=STATUS_SCHEDULED)
    passengers = EmbeddedDocumentListField(document_type='Passenger')
    updated_at = DateTimeField(default=arrow.utcnow().datetime)
    created_at = DateTimeField(default=arrow.utcnow().datetime)
    deleted_at = DateTimeField()

    def clean(self):
        self.updated_at = arrow.now().datetime
        self.__set_before_and_after_time()

    def cancel(self):
        self.status = STATUS_CANCELED
        self.deleted_at = arrow.now().datetime

    def update_time(self, time):
        self.time = time
        self.__set_before_and_after_time()

    def __set_before_and_after_time(self):
        time = arrow.get(self.time)
        is_departing = self.type

        self.start_time = time.shift(hours=-1).datetime if is_departing else time.shift(minutes=-15).datetime
        self.end_time = time.shift(minutes=+15).datetime if is_departing else time.shift(hours=+1).datetime

# class Flight(db.Entity, ParsingMixin):
#     nr = Required(int)
#     type = Required(bool)
#     location = Required(str)
#     airline = Required('Airline')
#     airplane = Required('Airplane')
#     start_time = Optional(datetime, volatile=True)
#     time = Required(datetime, volatile=True)
#     end_time = Optional(datetime, volatile=True)
#     status = Required(str, default='scheduled')
#     check_in_counter = Optional('CheckInCounter')
#     gate = Optional('Gate')
#     updated_at = Required(datetime, default=arrow.now().datetime, volatile=True)
#     created_at = Required(datetime, default=arrow.now().datetime, volatile=True)
#     deleted_at = Optional(datetime, volatile=True)
#
#     def cancel(self):
#         self.status = 'canceled'
#         self.deleted_at = arrow.now().datetime
#
#     def set_before_and_after_time(self):
#
#
#     def before_update(self):
#
#
#     def before_insert(self):
#         self.set_before_and_after_time()
#
#     def to_dict(self, *args, **kwargs):
#         dict = super().to_dict(*args, **kwargs)
#
#         for k,v in dict.items():
#             if isinstance(v, datetime):
#                 dict[k] = arrow.get(v).format('YYYY-MM-DD HH:mm:ss')
#
#         return dict
