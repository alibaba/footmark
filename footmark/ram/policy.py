
from footmark.ram.ramobject import TaggedRAMObject


class Policy(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Policy, self).__init__(connection)
        self.tags = {}

    def __getattr__(self, name):
        if name == 'name':
            return self.policy_name
        if name == 'type':
            return self.policy_type
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'name':
            self.policy_name = value
        if name == 'type':
            self.policy_type = value
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRAMObject, self).__setattr__(name, value)

    def delete(self):
        """
        delete the policy
        """
        return self.connection.delete_policy(self.policy_name)
