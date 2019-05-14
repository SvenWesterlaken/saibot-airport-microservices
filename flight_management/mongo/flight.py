from mongoengine import *
from .mixins import UpdateMixin, ParsableDocument
import arrow

STATUS_SCHEDULED = 0
STATUS_CANCELED = 1
STATUS_ARRIVED = 2
STATUS_DEPARTED = 3

class Flight(UpdateMixin, ParsableDocument):
    nr = IntField(required=True)
    type = BooleanField()
    location = StringField()
    start_time = DateTimeField()
    time = DateTimeField()
    end_time = DateTimeField()
    status = IntField(default=STATUS_SCHEDULED)
    airplane = EmbeddedDocumentField(document_type='Airplane')
    passengers = EmbeddedDocumentListField(document_type='Passenger')
    check_in_counter = EmbeddedDocumentField(document_type='CheckInCounter')
    gate = EmbeddedDocumentField(document_type='Gate')
    updated_at = DateTimeField(default=arrow.utcnow().datetime)
    created_at = DateTimeField(default=arrow.utcnow().datetime)
    deleted_at = DateTimeField()
    meta = {'collection': 'flights'}

    def clean(self):
        self.updated_at = arrow.now().datetime
        self.__set_before_and_after_time()

    def cancel(self):
        self.status = STATUS_CANCELED
        self.deleted_at = arrow.now().datetime
        self.save()

    def update_time(self, time):
        self.time = time
        self.__set_before_and_after_time()

    def __set_before_and_after_time(self):
        time = arrow.get(self.time)
        is_departing = self.type

        self.start_time = time.shift(hours=-1).datetime if is_departing else time.shift(minutes=-15).datetime
        self.end_time = time.shift(minutes=+15).datetime if is_departing else time.shift(hours=+1).datetime
