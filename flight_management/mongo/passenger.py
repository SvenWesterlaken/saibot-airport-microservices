from mongoengine import *

class Passenger(EmbeddedDocument):
    first_name = StringField()
    last_name = StringField()
    is_booker = BooleanField()
    email = EmailField()
    baggage = EmbeddedDocumentListField(document_type='Baggage')
