from footmark.regioninfo import RegionInfo


class DNSRegionInfo(RegionInfo):
    """
    Represents an DNS Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.dns.connection import DNSConnection
        super(DNSRegionInfo, self).__init__(connection, name, id,
                                            DNSConnection)

