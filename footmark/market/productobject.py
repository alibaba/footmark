class PRODUCTObject(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None


class TaggedPRODUCTObject(PRODUCTObject):
    def __init__(self, connection=None):
        super(TaggedPRODUCTObject, self).__init__(connection)
