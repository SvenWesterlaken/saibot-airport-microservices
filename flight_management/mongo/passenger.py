from mongoengine import *

passenger_schema = """
    properties:
        first_name:
            type: string
            example: John
            description: First name of the passenger
        last_name:
            type: string
            example: Doe
            description: Last name of the passenger
        is_booker:
            type: boolean
            default: false
            description: Whether this passenger is the booker (only the bookers will be notified of changes)
        email:
            type: string
            format: email
            description: Email of the passenger (only required and used if passenger is booker)
        baggage:
            type: array
            items:
                $ref: '#/definitions/Baggage'

"""

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
