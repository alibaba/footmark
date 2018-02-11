from footmark.regioninfo import RegionInfo


class OSSRegionInfo(RegionInfo):
    """
    Represents an OSS Region
    """

    def __init__(self, connection=None, name=None, id=None,
                 connection_cls=None):
        from footmark.oss.connection import OSSConnection
        super(OSSRegionInfo, self).__init__(connection, name, id,
                                            OSSConnection)
