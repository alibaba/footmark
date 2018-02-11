"""
Represents an ESS Scheduled Task
"""
from footmark.ess.essobject import TaggedESSObject


class ScheduledTask(TaggedESSObject):
    """
    Represents an scheduled task.
    """

    def __init__(self, connection=None):
        super(ScheduledTask, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'Scheduled Task: %s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.scheduled_task_id
        if name == 'name':
            return self.scheduled_task_name
        if name in ('scaling_rule_ari', 'rule_ari', 'ari'):
            return self.scheduled_action
        if name == 'launch_expiration':
            return self.launch_expiration_time
        if name == 'enabled':
            return self.task_enabled
        raise AttributeError("Object {0} does not have attribute {1}".format(self.__repr__(), name))

    def __setattr__(self, name, value):
        if name == 'id':
            self.scheduled_task_id = value
        if name == 'name':
            self.scheduled_task_name = value
        if name in ('scaling_rule_ari', 'rule_ari', 'ari'):
            self.scheduled_action = value
        if name == 'launch_expiration':
            self.launch_expiration_time = value
        if name == 'enabled':
            self.task_enabled = value
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
        rs = self.connection.describe_scheduled_tasks(scheduled_task_ids=[self.id])
        if len(rs) > 0:
            for r in rs:
                if r.id == self.id:
                    self._update(r)
        elif validate:
            raise ValueError('%s is not a valid Scheduled Task ID' % self.id)
        return self

    def modify(self, scaling_rule_ari=None, launch_time=None, name=None, description=None,
               launch_expiration_time=None, recurrence_type=None, recurrence_value=None,
               recurrence_end_time=None, task_enabled=None):
        """
        Modify the scheduled task
        """
        update = False
        if scaling_rule_ari and self.scaling_rule_ari != scaling_rule_ari:
            update = True
        if launch_time and self.launch_time != launch_time:
            update = True
        if name and self.name != name:
            update = True
        if description and getattr(self, 'description', None) and self.description != description:
            update = True
        if launch_expiration_time is not None and self.launch_expiration_time != launch_expiration_time:
            update = True
        if recurrence_type and self.recurrence_type != recurrence_type:
            update = True
        if recurrence_value and self.recurrence_value != recurrence_value:
            update = True
        if recurrence_end_time and self.recurrence_end_time != recurrence_end_time:
            update = True
        if task_enabled is not None and self.task_enabled != task_enabled:
            update = True

        if not update:
            return False

        return self.connection.modify_scheduled_task(self.id, scaling_rule_ari=scaling_rule_ari, launch_time=launch_time,
                                                     name=name, description=description, launch_expiration_time=launch_expiration_time,
                                                     recurrence_type=recurrence_type, recurrence_value=recurrence_value,
                                                     recurrence_end_time=recurrence_end_time, task_enabled=task_enabled)

    def terminate(self):
        """
        Terminate the scheduled task

        """
        return self.connection.terminate_scheduled_task(self.id)
