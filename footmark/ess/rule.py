"""
Represents an ESS Scaling Rule
"""
from footmark.ess.essobject import TaggedESSObject


class ScalingRule(TaggedESSObject):
    """
    Represents an scaling configuration.
    """

    def __init__(self, connection=None):
        super(ScalingRule, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Scaling Rule: %s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.scaling_rule_id
        if name in ('name', 'rule_name'):
            return self.scaling_rule_name
        if name == 'ari':
            return self.scaling_rule_ari
        if name == 'group_id':
            return self.scaling_group_id
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name in ('id', 'rule_id'):
            self.scaling_rule_id = value
        if name in ('name', 'rule_name'):
            self.scaling_rule_name = value
        if name == 'ari':
            self.scaling_rule_ari = value
        if name == 'group_id':
            self.scaling_group_id = value
        super(TaggedESSObject, self).__setattr__(name, value)

    def _update(self, updated):
        self.__dict__.update(updated.__dict__)

    def update(self, validate=False):
        """
        Update the instance's state information by making a call to fetch
        the current instance attributes from the service.scaling_rule_ids=None, scaling_rule_names=None

        :type validate: bool
        :param validate: By default, if ECS returns no data about the
                         instance the update method returns quietly.  If
                         the validate param is True, however, it will
                         raise a ValueError exception if no data is
                         returned from ECS.
        """
        rs = self.connection.describe_rules(scaling_rule_ids=[self.id])
        if len(rs) > 0:
            for r in rs:
                if r.id == self.id:
                    self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Scaling Rule ID' % self.id)
        return self

    def modify(self, adjustment_type=None, adjustment_value=None, name=None, cooldown=None):
        """
        modify the scaling rule

        :type force: bool
        :param force: Forces the instance to stop

        :rtype: bool
        :return: result of modifying
        """
        update = False
        if adjustment_type and self.adjustment_type != adjustment_type:
            update = True
        if adjustment_value and self.adjustment_value != adjustment_value:
            update = True
        if name and self.name != name:
            update = True
        if cooldown is not None and self.cooldown != cooldown:
            update = True

        if not update:
            return False

        return self.connection.modify_rule(self.id, adjustment_type=adjustment_type, adjustment_value=adjustment_value,
                                           name=name, cooldown=cooldown)

    def terminate(self):
        """
        Terminate the rule
        """
        return self.connection.terminate_rule(self.id)
