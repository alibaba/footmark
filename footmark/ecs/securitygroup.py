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

    def get(self):
        """
        Terminate the security group
        """
        return self.connection.get_security_group_attribute(self.id)

    def read(self):
        group = {}
        ingresses = []
        egresses  = []
        for name, value in self.__dict__.items():
            if name in ["connection", "region_id", "region", "request_id"]:
                continue

            if name == "security_group_id":
                group['id'] = value
                name = "group_id"

            if name == 'security_group_name':
                name = "group_name"

            if name == 'permissions':
                for rule in value:
                    if rule['direction'] == 'ingress':
                        ingresses.append(rule)
                    else:
                        egresses.append(rule)
                group[name] = ingresses
                group[name + '_egress'] = egresses
                continue

            group[name] = value
        return group