import uuid
import json


class RabbitmqMessage:

    def __init__(self, message, from_where, type, data, old_data):
        self.id = str(uuid.uuid4())
        self.message = message
        self.from_where = from_where
        self.type = type
        self.data = data
        self.old_data = old_data

    def to_json(self):
        return json.dumps(self.__dict__)
