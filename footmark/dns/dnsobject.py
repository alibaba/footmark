class DNSObject(object):
    def __init__(self, connection=None):
        self.connection = connection
        if self.connection and hasattr(self.connection, 'region'):
            self.region = connection.region
        else:
            self.region = None


class TaggedDNSObject(DNSObject):
    def __init__(self, connection=None):
        super(TaggedDNSObject, self).__init__(connection)
