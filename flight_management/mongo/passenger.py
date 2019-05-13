from mongoengine import *

class Passenger(EmbeddedDocument, UpdateMixin):
    first_name = StringField()
    last_name = StringField()
    is_booker = BooleanField()
    email = EmailField()
