from pony import orm
import json

db = orm.Database()

class ParsingMixin(object):

    def update_props(self, update):
        for key,value in update.items():
            setattr(self, key, value)
