from footmark.regioninfo import RegionInfo


class ECSRegionInfo(RegionInfo):
    """
    Represents an ECS Region
    """

    def __init__(self, connection=None):
        from footmark.ecs.connection import ECSConnection
        super(ECSRegionInfo, self).__init__(connection, connection_cls=ECSConnection)
