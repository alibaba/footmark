"""
Represents an ECS Instance Type
"""
from footmark.ecs.ecsobject import *


class InstanceType(TaggedECSObject):
    """
    Represents an instance type.
    """

    def __init__(self, connection=None):
        super(InstanceType, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'InstanceType:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.instance_type_id
        if name == 'family':
            return self.instance_type_family
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.instance_type_id = value
        if name == 'family':
            self.instance_type_family = value
        super(TaggedECSObject, self).__setattr__(name, value)


class InstanceTypeFamily(TaggedECSObject):
    """
       Represents an instance type family.
    """

    def __init__(self, connection=None):
        super(InstanceTypeFamily, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'InstanceTypeFamily:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.instance_type_family_id
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.instance_type_family_id = value
        super(TaggedECSObject, self).__setattr__(name, value)

