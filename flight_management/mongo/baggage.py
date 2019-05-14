from mongoengine import *

class Baggage(EmbeddedDocument):
    weight = IntField(required=True, default=0)
