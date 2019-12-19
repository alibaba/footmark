# encoding: utf-8
import json
from footmark.connection import ACSQueryConnection
from footmark.ram.regioninfo import RegionInfo
from footmark.exception import RAMResponseError
from footmark.ram.ram import User, Profile, Access, Group, Role, Policy
# from aliyunsdkram.request.v20150501.CreateRoleRequest import


class RAMConnection(ACSQueryConnection):
    SDKVersion = '2015-05-01'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = RAMResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None):
        """
        Init method to create a new connection to STS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.RAMSDK = 'aliyunsdkram.request.v' + self.SDKVersion.replace('-', '')

        super(RAMConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.RAMSDK,
                                            user_agent=user_agent,
                                            ecs_role_name=ecs_role_name)

    def list_users(self, **kwargs):
        results = []
        users = []
        is_truncated = True
        while is_truncated:
            res = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), User)
            users.extend(res.users['user'])
            is_truncated = res.is_truncated
            kwargs['marker'] = res.marker

        for user in users:
            element = User(self)
            for k, v in list(user.items()):
                setattr(element, k, v)
            results.append(element)
        return results

    def delete_user(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def create_user(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), User)

    def update_user(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), User)

    def get_login_profile(self, **kwargs):
        try:
            return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Profile)
        except:
            return None

    def create_login_profile(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Profile)

    def delete_login_profile(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def update_login_profile(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def create_access_key(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Access)

    def list_access_keys(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['AccessKeys', Access])

    def update_access_key(self, **kwargs):
        if self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs))):
            access_keys = self.list_access_keys(**kwargs)
            for access in access_keys:
                if kwargs['user_access_key_id'] == access.read()['access_key_id']:
                    return access
        return None

    def delete_access_key(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def create_group(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Group)

    def update_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def delete_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_groups(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Groups', Group])

    def add_user_to_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def remove_user_from_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_users_for_group(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Users', Group])

    def create_role(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Role)

    def list_roles(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Roles', Role])

    def get_role(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Role)

    def update_role(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def delete_role(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def create_policy(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Policy)

    def delete_policy(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def get_policy(self, **kwargs):
        if not kwargs.get('policy_type'):
            kwargs['policy_type'] = 'Custom'
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Policy)

    def attach_policy_to_user(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def attach_policy_to_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def attach_policy_to_role(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def detach_policy_from_user(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def detach_policy_from_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def detach_policy_from_role(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_policies(self, **kwargs):
        results = []
        policies = []
        is_truncated = True
        while is_truncated:
            res = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Policy)
            policies.extend(res.policies['policy'])
            is_truncated = res.is_truncated
            kwargs['marker'] = res.marker

        for policy in policies:
            element = Policy(self)
            for k, v in list(policy.items()):
                setattr(element, k, v)
            results.append(element)
        return results

    def list_policies_for_user(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Policies', Policy])

    def list_policies_for_group(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Policies', Policy])

    def list_policies_for_role(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Policies', Policy])

