from footmark.regioninfo import RegionInfo


class SLBRegionInfo(RegionInfo):
    """
    Represents an SLB Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.slb.connection import SLBConnection
        super(SLBRegionInfo, self).__init__(connection, name, id,
                                            SLBConnection)
