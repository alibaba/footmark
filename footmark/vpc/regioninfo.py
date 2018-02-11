from footmark.regioninfo import RegionInfo


class VPCRegionInfo(RegionInfo):
    """
    Represents an ECS Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.vpc.connection import VPCConnection
        super(VPCRegionInfo, self).__init__(connection, name, id,
                                            VPCConnection)
