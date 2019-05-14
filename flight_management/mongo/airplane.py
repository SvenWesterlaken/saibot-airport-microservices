from mongoengine import *

class Airplane(EmbeddedDocument):
    e_id = IntField(required=True)
    max_capacity = IntField(required=True)
    airline = StringField(required=True)
