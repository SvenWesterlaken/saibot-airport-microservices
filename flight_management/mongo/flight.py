from mongoengine import *
from itertools import chain
from .mixins import UpdateMixin, ParsableDocument
import numpy as np
import arrow

STATUS_SCHEDULED = 0
STATUS_CANCELED = 1
STATUS_ARRIVED = 2
STATUS_DEPARTED = 3

flight_schema = """
    properties:
        _id:
            type: string
            format: uuid
            example: 5cdc02bbe3dafee2a3538d8e
            description: ID of the flight
        nr:
            type: integer
            description: Number of the flight
            example: 102
        type:
            type: boolean
            description: Whether the flight is departing or not
        location:
            type: string
            example: 'Oakland, CA'
            description: Location where the flight is coming from / going to
        start_time:
            type: string
            example: 2019-05-15 10:58:00
            description: Start time when the gate needs to be free
        time:
            type: string
            example: 2019-05-15 11:13:00
            description: Time of actual departure/arrival for the flight
        end_time:
            type: string
            example: 2019-05-15 12:13:00
            description: End time when the gate needs to be free
        status:
            type: integer
            default: 0
            description: 'Status of the flight.\n\n0 = Scheduled\n\n1 = Canceled\n\n2 = Arrived\n\n3 = Departed'
        updated_at:
            type: string
            example: 2019-05-15 14:38:00
            description: Datetime when this object was last updated
        created_at:
            type: string
            example: 2019-05-15 14:38:00
            description: Datetime when this object was created
        deleted_at:
            type: string
            example: 2019-05-15 14:40:00
            description: Datetime when this object was soft deleted (ie. flight canceled)
        airplane:
            $ref: '#/definitions/Airplane'
        passengers:
            type: array
            items:
                $ref: '#/definitions/Passenger'
        check_in_counter:
            $ref: '#/definitions/CheckInCounter'
        gate:
            $ref: '#/definitions/Gate'
"""

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

    def to_parsable(self):
        dict = super().to_parsable()
        dict['total_weight'] = self.__weight_from_dict(dict)

        return dict

    def clean(self):
        self.updated_at = arrow.now().datetime
        self.__set_before_and_after_time()

    def cancel(self):
        self.status = STATUS_CANCELED
        self.deleted_at = arrow.now().datetime
        self.save()

    def __weight_from_dict(self, item):
        return int(np.sum(list(map(lambda b : b['weight'], chain.from_iterable([p['baggage'] for p in item['passengers']])))))

    def total_weight(self):
        return int(np.sum(list(map(lambda b : b.weight, chain.from_iterable([p.baggage for p in self.passengers])))))

    def update_time(self, time):
        self.time = time
        self.__set_before_and_after_time()

    def __set_before_and_after_time(self):
        time = arrow.get(self.time)
        is_departing = self.type

        self.start_time = time.shift(hours=-1).datetime if is_departing else time.shift(minutes=-15).datetime
        self.end_time = time.shift(minutes=+15).datetime if is_departing else time.shift(hours=+1).datetime
