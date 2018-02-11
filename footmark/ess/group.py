"""
Represents an ECS Instance
"""
from footmark.ess.essobject import TaggedESSObject


class ScalingGroup(TaggedESSObject):
    """
    Represents an scaling configuration.
    """

    def __init__(self, connection=None):
        super(ScalingGroup, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Scaling Group:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.scaling_group_id
        if name == 'name':
            return self.scaling_group_name
        if name in ('state', 'status'):
            return self.lifecycle_state
        if name in ('configuration_id', 'scaling_configuration_id'):
            return getattr(self, 'active_scaling_configuration_id', None)
        if name == 'cooldown':
            return self.default_cooldown
        if name in ('vswitch_id', 'subnet_id'):
            return getattr(self, 'v_switch_id', None)
        if name in ('vswitch_ids', 'subnet_ids'):
            return getattr(self, 'v_switch_ids', None)
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name == 'id':
            self.scaling_group_id = value
        if name == 'name':
            self.scaling_group_name = value
        if name == 'lifecycle_state':
            value = value.lower()
        if name in ('state', 'status'):
            self.lifecycle_state = value
        if name in ('configuration_id', 'scaling_configuration_id'):
            self.active_scaling_configuration_id = value
        if name == 'cooldown':
            self.default_cooldown = value
        if name in ('vswitch_id', 'subnet_id'):
            self.v_switch_id = value
        if name in ('vswitch_ids', 'subnet_ids'):
            self.v_switch_ids = value
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

    def enable(self, scaling_configuration_id=None, instance_ids=None):
        """
        Enable the scaling group.
        """
        return self.connection.enable_group(self.id, scaling_configuration_id=scaling_configuration_id, instance_ids=instance_ids)

    def disable(self):
        """
        Disable the scaling group

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instances stopped
        """
        return self.connection.disable_group(self.id)

    def modify(self, max_size=None, min_size=None, name=None, default_cooldown=None, removal_policies=None, scaling_configuration_id=None):
        """
        Stop the instance

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: list
        :return: A list of the instances stopped
        """
        if min_size:
            if not max_size:
                max_size = self.max_size
            if min_size > max_size:
                min_size = max_size

        return self.connection.modify_group(self.id, max_size=max_size, min_size=min_size, name=name, default_cooldown=default_cooldown,
                                            removal_policies=removal_policies, scaling_configuration_id=scaling_configuration_id)

    def terminate(self, force=False):
        """
        Terminate the instance

        :type force: bool
        :param force: Forces the instance to terminate
        """
        return self.connection.terminate_group(self.id, force=force)
