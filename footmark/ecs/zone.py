"""
Represents an ECS Zone
"""
from footmark.ecs.ecsobject import *


class Zone(TaggedECSObject):
    """
       Represents an instance type family.
    """

    def __init__(self, connection=None):
        super(Zone, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Zone:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.zone_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.zone_id = value
        super(TaggedECSObject, self).__setattr__(name, value)
