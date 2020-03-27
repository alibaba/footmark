class OOSObject(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None


class TaggedOOSObject(OOSObject):
    def __init__(self, connection=None):
        super(TaggedOOSObject, self).__init__(connection)
