"""
Represents an ECS Security Group
"""
from footmark.ecs.ecsobject import TaggedECSObject


class SecurityGroup(TaggedECSObject):
    def __init__(self, connection=None):
        super(SecurityGroup, self).__init__(connection)
        self.tags = {}

    def __repr__(self):
        return 'SecurityGroup:%s' % self.id

    def __getattr__(self, name):
        if name == 'id':
            return self.security_group_id
        if name == 'name':
            return self.security_group_name
        if name.startswith('group'):
            return getattr(self, 'security_' + name)
        if name == 'rules':
            return getattr(self, 'permissions')
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.security_group_id = value
        if name == 'name':
            self.security_group_name = value
        if name.startswith('group'):
            setattr(self, 'security_' + name, value)
        if name == "permissions":
            if value and 'permission' in value:
                value = value.get('permission')
        if name == "rules":
            setattr(self, 'permissions', value)
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def delete(self):
        """
        Terminate the security group
        """
        return self.connection.delete_security_group(self.id)
