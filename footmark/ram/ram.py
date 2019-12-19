"""
Represents an VPC Security Group
"""
from footmark.ram.ramobject import TaggedRAMObject


class User(TaggedRAMObject):
    def __init__(self, connection=None):
        super(User, self).__init__(connection)

    def __repr__(self):
        return 'Ram:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.user_name
        if name == 'mobile_phone':
            return self.phone

    def __setattr__(self, name, value):
        if name == 'user_name':
            self.name = value
        if name == 'user_id':
            self.id = value
        if name == 'mobile_phone':
            self.phone = value
        if name == 'user':
            for k, v in value.items():
                super(TaggedRAMObject, self).__setattr__(k, v)
        super(TaggedRAMObject, self).__setattr__(name, value)

    def read(self):
        ram = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'user':
                for k, v in value.items():
                    ram[k] = v
                    setattr(self, k, v)
                continue
            ram[name] = value
        return ram

    def delete(self):
        return self.connection.delete_user(UserName=self.name)

    def update(self, **kwargs):
        params = {}
        if kwargs.get('new_user_name') and kwargs.get('new_user_name') != self.name:
            params['new_user_name'] = kwargs.get('new_user_name')
        if kwargs.get('mobile_phone') and kwargs.get('mobile_phone') != self.mobile_phone:
            params['new_mobile_phone'] = kwargs.get('mobile_phone')
        if kwargs.get('display_name') and kwargs.get('display_name') != self.display_name:
            params['new_display_name'] = kwargs.get('display_name')
        if kwargs.get('email') and kwargs.get('email') != self.email:
            params['new_email'] = kwargs.get('email')
        if kwargs.get('comments') and kwargs.get('comments') != self.comments:
            params['new_comments'] = kwargs.get('comments')
        if params:
            params['user_name'] = self.name
            params['new_user_name'] = kwargs.get('new_user_name') if kwargs.get('new_user_name') else params['user_name']
            return self.connection.update_user(**params)
        return None


class Profile(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Profile, self).__init__(connection)

    def __repr__(self):
        return 'Profile:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.user_name

    def __setattr__(self, name, value):
        if name == 'user_name':
            self.name = value
        super(TaggedRAMObject, self).__setattr__(name, value)

    def get(self):
        return self.connection.get_login_profile(user_name=self.user_name)

    def read(self):
        ram = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'login_profile':
                for key, value in value.items():
                    ram[key] = value
                continue
            ram[name] = value
        return ram

    def delete(self):
        return self.connection.delete_login_profile(user_name=self.name)

    def update(self, **kwargs):
        if kwargs.get('password_reset_required') != self.login_profile['password_reset_required'] or kwargs.get('mfa_bind_required') != self.login_profile['mfabind_required'] or kwargs.get('new_password'):
            if kwargs.get('new_password'):
                kwargs['password'] = kwargs.get('new_password')
            return self.connection.update_login_profile(**kwargs)
        return False


class Access(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Access, self).__init__(connection)

    def __repr__(self):
        return 'Access:%s' % self.id

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        super(TaggedRAMObject, self).__setattr__(name, value)

    def read(self):
        access_key = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'access_key':
                for key, value in value.items():
                    access_key[key] = value
                continue
            access_key[name] = value
        return access_key


class Group(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Group, self).__init__(connection)

    def __repr__(self):
        return 'Group:%s' % self.id

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        if name == 'group_name':
            self.name = value
        super(TaggedRAMObject, self).__setattr__(name, value)

    def read(self):
        group = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            group[name] = value
        return group

    def delete(self):
        return self.connection.delete_group(group_name=self.name)

    def update(self, comments=None, new_group_name=None):
        params = {}
        if comments and comments != self.comments:
            params['new_comments'] = comments
        if new_group_name and new_group_name != self.name:
            params['new_group_name'] = new_group_name
        if params:
            params['group_name'] = self.name
            return self.connection.update_group(**params)
        return False

    def add_user(self, user_name=None):
        users = self.connection.list_users_for_group(group_name=self.name)
        flag = False
        for user in users:
            if user.user_name == user_name:
                flag = True
        if not flag:
            return self.connection.add_user_to_group(user_name=user_name, group_name=self.name)
        return False

    def remove_user(self, user_name=None):
        users = self.connection.list_users_for_group(group_name=self.name)
        flag = False
        for user in users:
            if user.user_name == user_name:
                flag = True
        if flag:
            return self.connection.remove_user_from_group(user_name=user_name, group_name=self.name)
        return False


class Role(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Role, self).__init__(connection)

    def __repr__(self):
        return 'Role:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.role_name

    def __setattr__(self, name, value):
        if name == 'role_name':
            self.name = value
        super(TaggedRAMObject, self).__setattr__(name, value)

    def read(self):
        role = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'role':
                for k, v in value.items():
                    role[k] = v
                continue
            role[name] = value
        return role

    def get(self):
        return self.connection.get_role(role_name=self.name)

    def delete(self):
        return self.connection.delete_role(role_name=self.name)

    def update_policy(self, policy=None):
        params = {}
        role_policy = self.connection.get_role(role_name=self.name).read()['assume_role_policy_document']
        role_policy = role_policy.replace('\n', '').replace(' ', '')
        policy = policy.replace('\n', '').replace(' ', '')
        if policy and policy != role_policy:
            params['new_assume_role_policy_document'] = policy
        if params:
            params['role_name'] = self.name
            return self.connection.update_role(**params)
        return False


class Policy(TaggedRAMObject):
    def __init__(self, connection=None):
        super(Policy, self).__init__(connection)

    def __repr__(self):
        return 'Policy:%s' % self.id

    def __getattr__(self, name):
        if name == 'name':
            return self.policy_name

    def __setattr__(self, name, value):
        if name == 'policy_name':
            self.name = value
        super(TaggedRAMObject, self).__setattr__(name, value)

    def read(self):
        policy = {}
        for name, value in list(self.__dict__.items()):
            if name in ["connection", "region_id", "region", "request_id"]:
                continue
            if name == 'policy':
                for k, v in value.items():
                    policy[k] = v
                continue
            if name == 'policy_name':
                policy['name'] = value
            # if name == 'policies':
            #     for k, v in value.items():
            #         policy[k] = v
            #     continue
            policy[name] = value
        return policy

    # def get(self):
    #     return self.connection.get_role(role_name=self.name)

    def delete(self):
        return self.connection.delete_policy(policy_name=self.name)

    def attach_policy_to_user(self, user_name=None, policy_type=None):
        policy_user = self.connection.list_policies_for_user(user_name=user_name)
        params = {'policy_name': self.name}
        attach = True
        for policy in policy_user:
            if policy.name == self.name:
                attach = False
        if attach:
            params['user_name'] = user_name
            params['policy_type'] = policy_type
            return self.connection.attach_policy_to_user(**params)
        return False

    def attach_policy_to_group(self, group_name=None, policy_type=None):
        policy_group = self.connection.list_policies_for_group(group_name=group_name)
        params = {'policy_name': self.name}
        attach = True
        for policy in policy_group:
            if policy.name == self.name:
                attach = False
        if attach:
            params['group_name'] = group_name
            params['policy_type'] = policy_type
            return self.connection.attach_policy_to_group(**params)
        return False

    def attach_policy_to_role(self, role_name=None, policy_type=None):
        policy_role = self.connection.list_policies_for_role(role_name=role_name)
        params = {'policy_name': self.name}
        attach = True
        for policy in policy_role:
            if policy.name == self.name:
                attach = False
        if attach:
            params['role_name'] = role_name
            params['policy_type'] = policy_type
            return self.connection.attach_policy_to_role(**params)
        return False

    def detach_policy_from_user(self, user_name=None, policy_type=None):
        policy_user = self.connection.list_policies_for_user(user_name=user_name)
        params = {'policy_name': self.name}
        detach = False
        for policy in policy_user:
            if policy.name == self.name:
                detach = True
        if detach:
            params['user_name'] = user_name
            params['policy_type'] = policy_type
            return self.connection.detach_policy_from_user(**params)
        return False

    def detach_policy_from_group(self, group_name=None, policy_type=None):
        policy_group = self.connection.list_policies_for_group(group_name=group_name)
        params = {'policy_name': self.name}
        detach = False
        for policy in policy_group:
            if policy.name == self.name:
                detach = True
        if detach:
            params['group_name'] = group_name
            params['policy_type'] = policy_type
            return self.connection.detach_policy_from_group(**params)
        return False

    def detach_policy_from_role(self, role_name=None, policy_type=None):
        policy_role = self.connection.list_policies_for_role(role_name=role_name)
        params = {'policy_name': self.name}
        detach = False
        for policy in policy_role:
            if policy.name == self.name:
                detach = True
        if detach:
            params['role_name'] = role_name
            params['policy_type'] = policy_type
            return self.connection.detach_policy_from_role(**params)
        return False
