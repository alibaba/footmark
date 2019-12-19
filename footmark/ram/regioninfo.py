from footmark.regioninfo import RegionInfo


class RAMRegionInfo(RegionInfo):
    """
    Represents an RAM Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.ram.connection import RAMConnection
        super(RAMRegionInfo, self).__init__(connection, name, id,
                                            RAMConnection)

