from mongoengine import *

class Gate(EmbeddedDocument):
    e_id = IntField(required=True)
    terminal = StringField(max_length=1, required=True)
    nr = IntField(required=True)
