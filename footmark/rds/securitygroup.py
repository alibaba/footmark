"""
Represents an RDS Security Group
"""
from footmark.rds.rdsobject import TaggedRDSObject


class SecurityGroup(TaggedRDSObject):
    def __init__(self, connection=None, owner_id=None,
                 name=None, description=None, id=None):
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
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'id':
            self.security_group_id = value
        if name == 'name':
            self.security_group_name = value
        if name.startswith('group'):
            return setattr(self, 'security_' + name, value)
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedRDSObject, self).__setattr__(name, value)
