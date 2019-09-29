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
        if name == 'ip_protocol':
            value = str(value).lower()
        if name == 'tags' and value:
            v = {}
            for tag in value['tag']:
                v[tag.get('TagKey')] = tag.get('TagValue', None)
            value = v
        super(TaggedECSObject, self).__setattr__(name, value)

    def modify(self, name=None, description=None):
        params = {}
        if name and self.security_group_name != name:
            params['security_group_name'] = name
        if description and self.description != description:
            params['description'] = description
        if params:
            params['security_group_id'] = self.id
            return self.connection.modify_security_group_attribute(**params)
        return False

    def authorize(self, rule, direction):

        if not isinstance(rule, dict):
            module.fail_json(msg='Invalid rule parameter type [{0}].'.format(type(rule)))

        find = False
        for per in self.permissions:
            if per.get('direction', "") != direction:
                continue
            for key, value in list(rule.items()):
                if value != per.get(key, ""):
                    find = False
                    break
                find = True
            if find:
                break
        # If the rule is in the group, return directly.
        if find:
            return False
        params = {}
        for k, v in list(rule.items()):
            params[k] = v
        params["security_group_id"] = self.id
        if direction == 'ingress':
            return self.connection.authorize_security_group(**params)
        return self.connection.authorize_security_group_egress(**params)

    def revoke(self, rule, direction):

        if not isinstance(rule, dict):
            module.fail_json(msg='Invalid rule parameter type [{0}].'.format(type(rule)))

        find = False
        for per in self.permissions:
            if per.get('direction', "") != direction:
                continue
            for key, value in list(rule.items()):
                if value != per.get(key, ""):
                    find = False
                    break
                find = True
            if find:
                break
        # If the rule is not in the group, return directly.
        if not find:
            return False
        params = {}
        for k, v in list(rule.items()):
            params[k] = v
        params["security_group_id"] = self.id
        if direction == 'ingress':
            return self.connection.revoke_security_group(**params)
        return self.connection.revoke_security_group_egress(**params)

    def delete(self):
        """
        Terminate the security group
        """
        return self.connection.delete_security_group(security_group_id=self.id)

    def get(self):
        """
        Terminate the security group
        """
        return self.connection.describe_security_group_attribute(security_group_id=self.id)

    def read(self):
        group = {}
        ingresses = []
        egresses = []
        for name, value in list(self.__dict__.items()):
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