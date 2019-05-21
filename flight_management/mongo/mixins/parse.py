from mongoengine import *
import bson, datetime, arrow

class ParsableDocument(Document):
    meta = {'abstract': True}

    def __convert_prop_type(self, prop):

        if isinstance(prop, datetime.datetime):
            return arrow.get(prop).format('YYYY-MM-DD HH:mm:ss')
        elif isinstance(prop, bson.objectid.ObjectId):
            return str(prop)
        else:
            return prop

    def to_parsable(self):
        dict = self.to_mongo().to_dict()

        for key, value in dict.items():
            dict[key] = self.__convert_prop_type(value)

        return dict
