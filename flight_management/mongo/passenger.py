from mongoengine import *

class Passenger(EmbeddedDocument):
    first_name = StringField()
    last_name = StringField()
    is_booker = BooleanField(required=True, default=False)
    email = EmailField()
    baggage = EmbeddedDocumentListField(document_type='Baggage')

    def clean(self):
        """Check if booker has an required email. If not, raise an error"""
        if self.is_booker and self.email is None:
            raise ValidationError('Booker should have an email in order to contact them')
