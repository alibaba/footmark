"""
Represents an ECS Instance
"""
from footmark.ess.essobject import TaggedESSObject


class ScalingInstance(TaggedESSObject):
    """
    Represents an scaling configuration.
    """

    def __init__(self, connection=None):
        super(ScalingInstance, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Scaling Instance:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.instance_id
        if name in ('state', 'status'):
            return self.lifecycle_state
        if name in ('configuration_id', 'scaling_configuration_id'):
            return getattr(self, 'active_scaling_configuration_id', None)
        if name == 'group_id':
            return self.scaling_group_id
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name == 'id':
            self.instance_id = value
        if name == 'lifecycle_state':
            value = value.lower()
        if name in ('state', 'status'):
            self.lifecycle_state = value
        if name in ('configuration_id', 'scaling_configuration_id'):
            self.active_scaling_configuration_id = value
        if name == 'group_id':
            self.scaling_group_id = value
        super(TaggedESSObject, self).__setattr__(name, value)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the instance's state information by making a call to fetch
        the current instance attributes from the service.scaling_group_ids=None, scaling_group_names=None

        :type validate: bool
        :param validate: By default, if ECS returns no data about the
                         instance the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from ECS.
        """
        rs = self.connection.describe_groups(scaling_group_ids=[self.id])
        if len(rs) > 0:
            for r in rs:
                if r.id == self.id:
                    self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Scaling Configuration ID' % self.id)
        return self.state

