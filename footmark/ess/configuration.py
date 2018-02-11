"""
Represents an ECS Instance
"""
from footmark.ess.essobject import TaggedESSObject


class ScalingConfiguration(TaggedESSObject):
    """
    Represents an scaling configuration.
    """

    def __init__(self, connection=None):
        super(ScalingConfiguration, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Scaling Configuration:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.scaling_configuration_id
        if name == 'name':
            return self.scaling_configuration_name
        if name == 'group_id':
            return self.scaling_group_id
        if name in ('state', 'status'):
            return self.lifecycle_state
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name == 'id':
            self.scaling_configuration_id = value
        if name == 'name':
            self.scaling_configuration_name = value
        if name == 'group_id':
            self.scaling_group_id = value
        if name == 'lifecycle_state':
            value = value.lower()
        if name in ('state', 'status'):
            self.lifecycle_state = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                if tag.get('tag_key'):
                    v[tag.get('tag_key')] = tag.get('tag_value', None)
            value = v
        super(TaggedESSObject, self).__setattr__(name, value)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the instance's state information by making a call to fetch
        the current instance attributes from the service.

        :type validate: bool
        :param validate: By default, if ECS returns no data about the
                         instance the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from ECS.
        """
        rs = self.connection.describe_configurations(self.scaling_group_id, [self.id])
        if len(rs) > 0:
            for r in rs:
                if r.id == self.id:
                    self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Scaling Configuration ID' % self.id)
        return self.state

    def active(self):
        """
        Start the instance.
        """
        return self.connection.start_instances([self.id])

    def inactive(self, force=False):
        """
        Stop the instance

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instances stopped
        """
        return self.connection.stop_instances([self.id], force)

    def terminate(self):
        """
        Terminate the instance

        :type force: bool
        :param force: Forces the instance to terminate
        """
        return self.connection.terminate_configuration(self.id)
