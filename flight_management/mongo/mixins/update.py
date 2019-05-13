class UpdateMixin(object):

    def update_props(self, update):
        for key,value in update.items():
            setattr(self,key,value)
