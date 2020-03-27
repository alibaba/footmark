from footmark.regioninfo import RegionInfo


class OOSRegionInfo(RegionInfo):
    """
    Represents an RAM Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.oos.connection import OOSConnection
        super(OOSRegionInfo, self).__init__(connection, name, id,
                                            OOSConnection)
