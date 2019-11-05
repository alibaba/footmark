class STSObject(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None


class TaggedSTSObject(STSObject):
    def __init__(self, connection=None):
        super(TaggedSTSObject, self).__init__(connection)
