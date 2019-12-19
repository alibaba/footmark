class RAMObject(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None


class TaggedRAMObject(RAMObject):
    def __init__(self, connection=None):
        super(TaggedRAMObject, self).__init__(connection)
