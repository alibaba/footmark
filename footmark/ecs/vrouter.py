"""
Represents an VRouter object
"""
from footmark.ecs.ecsobject import TaggedECSObject


class VRouterList(TaggedECSObject):
    def __init__(self, connection=None):
        super(VRouterList, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'VRouterList'

    def __setattr__(self, name, value):
        super(TaggedECSObject, self).__setattr__(name, value)
