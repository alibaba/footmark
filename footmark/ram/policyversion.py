
from footmark.ram.ramobject import TaggedRAMObject


class PolicyVersion(TaggedRAMObject):
    def __init__(self, connection=None):
        super(PolicyVersion, self).__init__(connection)
        self.tags = {}

    def __setattr__(self, name, value):
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
        return self.connection.delete_policy_ver(self.policy_name, self.version_id)
