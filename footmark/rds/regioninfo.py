from footmark.regioninfo import RegionInfo


class RDSRegionInfo(RegionInfo):
    """
    Represents an RDS Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.rds.connection import RDSConnection
        super(RDSRegionInfo, self).__init__(connection, name, id,
                                            RDSConnection)
