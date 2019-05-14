from mongoengine import *

class CheckInCounter(EmbeddedDocument):
    e_id = IntField(required=True)
    nr = IntField(required=True)
