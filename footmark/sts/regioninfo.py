from footmark.regioninfo import RegionInfo


class STSRegionInfo(RegionInfo):
    """
    Represents an RAM Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.sts.connection import STSConnection
        super(STSRegionInfo, self).__init__(connection, name, id,
                                            STSConnection)

