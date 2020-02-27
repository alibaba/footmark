from footmark.regioninfo import RegionInfo


class MARKETRegionInfo(RegionInfo):
    """
    Represents an MARKET Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.market.connection import MARKETConnection
        super(MARKETRegionInfo, self).__init__(connection, name, id,
                                               MARKETConnection)

