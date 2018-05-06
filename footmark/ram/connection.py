# encoding: utf-8
"""
Represents a connection to the RAM service.
"""
import six

from footmark.connection import ACSQueryConnection
from footmark.ram.group import Group
from footmark.ram.loginprofile import LoginProfile
from footmark.ram.mfadevice import MfaDevice
from footmark.ram.policy import Policy
from footmark.ram.policyversion import PolicyVersion
from footmark.ram.regioninfo import RegionInfo
from footmark.exception import RamResponseError
from footmark.ram.role import Role
from footmark.ram.user import User
from footmark.resultset import ResultSet
from footmark.ram.accesskey import AccessKey


class RAMConnection(ACSQueryConnection):
    SDKVersion = '2015-05-01'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    RamResponseError = RamResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to RAM.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.RAMSDK = 'aliyunsdkram.request.v' + self.SDKVersion.replace('-', '')

        super(RAMConnection, self).__init__(acs_access_key_id,
                                            acs_secret_access_key,
                                            self.region, self.RAMSDK, security_token, user_agent=user_agent)

    def create_access_key(self, user_name):
        """
        add access_key for user
        :type user_name: str
        :param user_name: the name of user
        
        :rtype: object
        :return: Returns a <footmark.ram.accesskey> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_object('CreateAccessKey', params, AccessKey)

    def update_access_key(self, user_name, access_key_id, is_active=None):
        """
        update access_key for user
        
        :type user_name: str
        :param user_name: the name of user
        :type is_active: bool
        :param is_active: the status of accesskey
        
        :rtype: bool
        :return: The result of update  access_key.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, access_key_id, 'UserAccessKeyId')
        if is_active is True:
            self.build_list_params(params, 'Active', 'Status')
        else:
            self.build_list_params(params, 'Inactive', 'Status')

        return self.get_status('UpdateAccessKey', params)

    def delete_access_key(self, user_name, access_key_id):
        """
        delete access_key of user
        
        :type user_name: str
        :param user_name: the name of user
        :type access_key_id: str
        :param access_key_id: The access_key to delete
        
        :rtype: bool
        :return: The result of deleting  access_key.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, access_key_id, 'UserAccessKeyId')

        return self.get_status('DeleteAccessKey', params)

    def list_access_keys(self, user_name):
        """
        Retrieve all the access_key associated with your account.

        :type user_name: str
        :param user_name: User name of access_key

        :rtype: list
        :return: A list of  :class:`footmark.ram.accesskey`
        """
        params = {}
        if user_name:
            self.build_list_params(params, user_name, 'UserName')

        return self.get_list('ListAccessKeys', params, ['AccessKeys', AccessKey])

    def create_user(self, user_name, display_name=None, phone=None, email=None, comments=None):
        """
        create user
        
        :type user_name: str
        :param user_name: The name of user
        :type display_name: str
        :param display_name: The display name of user
        :type phone: str
        :param phone: The phone of user
        :type email: str
        :param email: The email of user
        :type comments: str
        :param comments: The comments about user
        
        :rtype: object
        :return: Returns a <footmark.ram.user> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        if display_name:
            self.build_list_params(params, display_name, 'DisplayName')
        if phone:
            self.build_list_params(params, phone, 'MobilePhone')
        if email:
            self.build_list_params(params, email, 'Email')
        if comments:
            self.build_list_params(params, comments, 'Comments')

        return self.get_object('CreateUser', params, User)

    def get_user(self, user_name):
        """
        get user

        :type user_name: str
        :param user_name: The name of user
        
        :rtype: object
        :return: Returns a <footmark.ram.user> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_object('GetUser', params, User)

    def update_user(self, user_name, new_display_name=None, new_user_name=None, new_phone=None, new_email=None, new_comments=None):
        """
        update user's info

        :type user_name: str
        :param user_name: The name of user
        :type new_user_name: str
        :param new_user_name: The new name of user
        :type new_display_name: str
        :param new_display_name: The new display name of user
        :type new_phone: str
        :param new_phone: The new phone of user
        :type new_email: str
        :param new_email: The new email of user
        :type new_comments: str
        :param new_comments: The new comments about user

        :rtype: bool
        :return: The result of update  user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        if new_user_name:
            self.build_list_params(params, new_user_name, 'NewUserName')
        if new_display_name:
            self.build_list_params(params, new_display_name, 'NewDisplayName')
        if new_phone:
            self.build_list_params(params, new_phone, 'NewMobilePhone')
        if new_email:
            self.build_list_params(params, new_email, 'NewEmail')
        if new_comments:
            self.build_list_params(params, new_comments, 'NewComments')

        return self.get_status('UpdateUser', params)

    def list_user(self):
        """
        Retrieve all the users associated with your account.

        :rtype: list
        :return: A list of  :class:`footmark.ram.user`
        """
        return self.get_list('ListUsers', None, ['Users', User])

    def delete_user(self, user_name):
        """
        delete user
        :type user_name: str
        :param user_name: the name of user
        
        :rtype: bool
        :return: The result of deleting  user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_status('DeleteUser', params)

    def create_role(self, role_name, policy_doc, description=None):
        """
        create role

        :type role_name: str
        :param role_name: The name of role
        :type policy_doc: str
        :param policy_doc: The policy document to assume role
        :type description: str
        :param description: The description of role
        
        :rtype: object
        :return: Returns a <footmark.ram.role> object.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')
        self.build_list_params(params, policy_doc, 'AssumeRolePolicyDocument')
        if description:
            self.build_list_params(params, description, 'Description')

        return self.get_object('CreateRole', params, Role)

    def get_role(self, role_name):
        """
        get role

        :type role_name: str
        :param role_name: The name of role

        :rtype: object
        :return: Returns a <footmark.ram.role> object.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')

        return self.get_object('GetRole', params, Role)

    def update_role(self, role_name, new_policy_doc=None):
        """
        update role's info

        :type role_name: str
        :param user_name: The name of role
        :type new_policy_doc: str
        :param new_policy_doc: The new policy of role

        :rtype: bool
        :return: The result of update  role.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')
        if new_policy_doc:
            self.build_list_params(params, new_policy_doc, 'NewAssumeRolePolicyDocument')

        return self.get_status('UpdateRole', params)

    def list_role(self):
        """
        Retrieve all the role associated with your account.

        :rtype: list
        :return: A list of  :class:`footmark.ram.role`
        """
        return self.get_list('ListRoles', None, ['Roles', Role])

    def delete_role(self, role_name):
        """
        delete role
        :type role_name: str
        :param role_name: the name of role

        :rtype: bool
        :return: The result of deleting  role.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')

        return self.get_status('DeleteRole', params)

    def create_group(self, group_name, comments=None):
        """
        create group

        :type group_name: str
        :param group_name: The name of group
        :type comments: str
        :param comments: The description of group
        
        :rtype: object
        :return: Returns a <footmark.ram.group> object.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')
        if comments:
            self.build_list_params(params, comments, 'Comments')

        return self.get_object('CreateGroup', params, Group)

    def get_group(self, group_name):
        """
        get group

        :type group_name: str
        :param group_name: The name of group

        :rtype: object
        :return: Returns a <footmark.ram.role> object.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_object('GetGroup', params, Group)

    def update_group(self, group_name, new_group_name=None, new_comments=None):
        """
        update group's info

        :type group_name: str
        :param group_name: The name of group
        :type new_group_name: str
        :param new_group_name: The new name of group
        :type new_comments: str
        :param new_comments: The new comments of group

        :rtype: bool
        :return: The result of update  group.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')
        if new_group_name:
            self.build_list_params(params, new_group_name, 'NewGroupName')
        if new_comments:
            self.build_list_params(params, new_comments, 'NewComments')

        return self.get_status('UpdateGroup', params)

    def list_group(self):
        """
        Retrieve all the group associated with your account.

        :rtype: list
        :return: A list of  :class:`footmark.ram.group`
        """
        return self.get_list('ListGroups', None, ['Groups', Group])

    def delete_group(self, group_name):
        """
        delete group
        :type group_name: str
        :param group_name: the name of group

        :rtype: bool
        :return: The result of deleting  group.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_status('DeleteGroup', params)

    def create_login_profile(self, user_name, pwd, pwd_reset_req=None, mfa_req=None):
        """
        create login_profile

        :type user_name: str
        :param user_name: The name of user
        :type pwd: str
        :param pwd: The password of user
        :type pwd_reset_req: bool
        :param pwd_reset_req: Whether to enable user reset password,the default value is false.
        :type mfa_req: bool
        :param mfa_req: Whether to enable user bind mfa,the default value is false.

        :rtype: object
        :return: Returns a <footmark.ram.loginprofile> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, pwd, 'Password')
        if pwd_reset_req is False or pwd_reset_req is None:
            self.build_list_params(params, False, 'PasswordResetRequired')
        if mfa_req is False or mfa_req is None:
            self.build_list_params(params, False, 'MFABindRequired')

        return self.get_object('CreateLoginProfile', params, LoginProfile)

    def get_login_profile(self, user_name):
        """
        get login_profile

        :type user_name: str
        :param user_name: The name of user

        :rtype: object
        :return: Returns a <footmark.ram.loginprofile> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_object('GetLoginProfile', params, LoginProfile)

    def update_login_profile(self, user_name, pwd=None, pwd_reset_req=None, mfa_req=None):
        """
        update login_profile's info

        :type user_name: str
        :param user_name: The name of user
        :type pwd: str
        :param pwd: The password of user
        :type pwd_reset_req: bool
        :param pwd_reset_req: Whether to enable user reset password,the default value is false.
        :type mfa_req: bool
        :param mfa_req: Whether to enable user bind mfa,the default value is false.

        :rtype: bool
        :return: The result of update  group.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        if pwd:
            self.build_list_params(params, pwd, 'Password')
        if pwd_reset_req is not None:
            self.build_list_params(params, pwd_reset_req, 'PasswordResetRequired')
        if mfa_req is not None:
            self.build_list_params(params, mfa_req, 'MFABindRequired')

        return self.get_status('UpdateLoginProfile', params)

    def delete_login_profile(self, user_name):
        """
        delete login_profile
        :type user_name: str
        :param user_name: the name of user

        :rtype: bool
        :return: The result of deleting  login_profile of user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_status('DeleteLoginProfile', params)

    def create_mfa_device(self, mfa_name):
        """
        create mfa_device

        :type mfa_name: str
        :param user_name: The name of mfa_device

        :rtype: object
        :return: Returns a <footmark.ram.mfadevice> object.
        """
        params = {}
        self.build_list_params(params, mfa_name, 'VirtualMFADeviceName')

        return self.get_object('CreateVirtualMFADevice', params, MfaDevice)

    def list_mfa_device(self):
        """
        Retrieve all the mfa devices associated with your account.

        :rtype: object
        :return: A list of  :class:`footmark.ram.mfadevice`
        """

        return self.get_list('ListVirtualMFADevices', None, ['VirtualMFADevices', MfaDevice])

    def delete_mfa_device(self, serial_number):
        """
        delete mfa_device
        
        :type serial_number: str
        :param serial_number: the serial_number of mfa_device

        :rtype: bool
        :return: The result of deleting  mfa_device.
        """
        params = {}
        self.build_list_params(params, serial_number, 'SerialNumber')

        return self.get_status('DeleteVirtualMFADevice', params)

    def create_policy(self, policy_name, policy_doc, description=None):
        """
        create role

        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_doc: str
        :param policy_doc: The policy document
        :type description: str
        :param description: The description of policy

        :rtype: object
        :return: Returns a <footmark.ram.role> object.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_doc, 'PolicyDocument')
        if description:
            self.build_list_params(params, description, 'Description')

        return self.get_object('CreatePolicy', params, Policy)

    def get_policy(self, policy_name, policy_type):
        """
        get policy

        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: object
        :return: Returns a <footmark.ram.policy> object.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_object('GetPolicy', params, Policy)

    def list_policy(self, policy_type):
        """
        get policy

        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: object
        :return: A list of  :class:`footmark.ram.policy`
        """
        params = {}
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_list('ListPolicies', params, ['Policies', Policy])

    def delete_policy(self, policy_name):
        """
        delete policy
        :type policy_name: str
        :param policy_name: the name of policy

        :rtype: bool
        :return: The result of deleting  policy.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')

        return self.get_status('DeletePolicyName', params)

    def create_policy_ver(self, policy_name, policy_doc, as_default=None):
        """
        create role

        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_doc: str
        :param policy_doc: The policy document
        :type as_default: bool
        :param as_default: Enable as default policy,default false

        :rtype: object
        :return: Returns a <footmark.ram.policyversion> object.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_doc, 'PolicyDocument')
        if as_default is True :
            self.build_list_params(params, True, 'SetAsDefault')

        return self.get_object('CreatePolicyVersion', params, PolicyVersion)

    def get_policy_ver(self, policy_name, policy_type, version_id):
        """
        get policy with version

        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom
        :type version_id: str
        :param version_id: The version of policy

        :rtype: object
        :return: Returns a <footmark.ram.policyversion> object.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')
        self.build_list_params(params, version_id, 'VersionId')

        return self.get_object('GetPolicyVersion', params, PolicyVersion)

    def list_policy_ver(self, policy_name, policy_type):
        """
        get policy

        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: object
        :return: A list of  :class:`footmark.ram.policyversion`
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_list('ListPolicyVersions', params, ['PolicyVersions', PolicyVersion])

    def delete_policy_ver(self, policy_name, version_id):
        """
        delete policy with version
        :type policy_name: str
        :param policy_name: the name of policy
        :type version_id: str
        :param version_id: the version of policy

        :rtype: bool
        :return: The result of deleting  policy with version.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, version_id, 'VersionId')

        return self.get_status('DeletePolicyVersion', params)

    def bind_mfa_device(self, serial_number, user_name):
        """
        bind a device to a user

        :type user_name: str
        :param user_name: The name of user
        :type serial_number: str
        :param serial_number: the serial_number of mfa_device
        
        :rtype: bool
        :return: The result of bind  mfa_device to a user.
        """
        params = {}
        self.build_list_params(params, serial_number, 'SerialNumber')
        self.build_list_params(params, user_name, 'UserName')

        return self.get_status('BindMFADevice', params)

    def unbind_mfa_device(self, user_name):
        """
        unbind a device to a user

        :type user_name: str
        :param user_name: The name of user

        :rtype: bool
        :return: The result of unbind  mfa_device to a user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_status('UnbindMFADevice', params)

    def get_user_mfa_device(self, user_name):
        """
        unbind a device to a user

        :type user_name: str
        :param user_name: The name of user

        :rtype: object
        :return: Returns a <footmark.ram.mfadevice> object.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_object('GetUserMFAInfo', params, MfaDevice)

    def change_pwd(self, old_pwd, new_pwd):
        """
        delete policy with version
        
        :type old_pwd: str
        :param old_pwd: The old password
        :type new_pwd: str
        :param new_pwd: The new password

        :rtype: bool
        :return: The result of change password.
        """
        params = {}
        self.build_list_params(params, old_pwd, 'OldPassword')
        self.build_list_params(params, new_pwd, 'NewPassword')

        return self.get_status('ChangePassword', params)

    def attach_user_to_group(self, user_name, group_name):
        """
        attach a user to a group
        
        :type user_name: str
        :param user_name: The name of user
        :type group_name: str
        :param group_name: The name of group

        :rtype: bool
        :return: The result add a user to a group.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_status('AddUserToGroup', params)

    def detach_user_from_group(self, user_name, group_name):
        """
        detach a user from a group

        :type user_name: str
        :param user_name: The name of user
        :type group_name: str
        :param group_name: The name of group

        :rtype: bool
        :return: The result detach a user from group.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_status('RemoveUserFromGroup', params)

    def list_group_user(self, group_name):
        """
        Retrieve all the users associated with the group.
        
        :type group_name: str
        :param group_name: The name of group

        :rtype: list
        :return: A list of  :class:`footmark.ram.user`
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_list('ListUsersForGroup', params, ['Users', User])

    def list_user_group(self, user_name):
        """
        Retrieve all the users associated with the group.

        :type user_name: str
        :param user_name: The name of user

        :rtype: list
        :return: A list of  :class:`footmark.ram.user`
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_list('ListGroupsForUser', params, ['Groups', Group])

    def set_default_policy_ver(self, policy_name, version_id):
        """
        set default policy with version

        :type policy_name: str
        :param policy_name: The name of policy
        :type version_id: str
        :param version_id: The version of policy

        :rtype: bool
        :return: The result add a user to a group.
        """
        params = {}
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, version_id, 'VersionId')

        return self.get_status('SetDefaultPolicyVersion', params)

    def attach_policy_to_user(self, user_name, policy_name, policy_type):
        """
        attach a policy to a user

        :type user_name: str
        :param user_name: The name of user
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('AttachPolicyToUser', params)

    def detach_policy_from_user(self, user_name, policy_name, policy_type):
        """
        detach a policy from o a user

        :type user_name: str
        :param user_name: The name of user
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a user.
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('DetachPolicyFromUser', params)

    def attach_policy_to_group(self, group_name, policy_name, policy_type):
        """
        attach a policy to a group

        :type group_name: str
        :param group_name: The name of group
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a group.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('AttachPolicyToGroup', params)

    def detach_policy_from_group(self, group_name, policy_name, policy_type):
        """
        detach policy from a group

        :type group_name: str
        :param group_name: The name of group
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a user.
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('DetachPolicyFromGroup', params)

    def attach_policy_to_role(self, role_name, policy_name, policy_type):
        """
        attach a policy to a role

        :type role_name: str
        :param role_name: The name of role
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a role.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('AttachPolicyToRole', params)

    def detach_policy_from_role(self, role_name, policy_name, policy_type):
        """
        detach policy from a group

        :type role_name: str
        :param role_name: The name of role
        :type policy_name: str
        :param policy_name: The name of policy
        :type policy_type: str
        :param policy_type: The type of policy, System or Custom

        :rtype: bool
        :return: The result add a policy to a role.
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')
        self.build_list_params(params, policy_name, 'PolicyName')
        self.build_list_params(params, policy_type, 'PolicyType')

        return self.get_status('DetachPolicyFromRole', params)

    def list_policy_for_user(self, user_name):
        """
        get policy for user

        :type user_name: str
        :param user_name: The name of user

        :rtype: object
        :return: A list of  :class:`footmark.ram.policy`
        """
        params = {}
        self.build_list_params(params, user_name, 'UserName')

        return self.get_list('ListPoliciesForUser', params, ['Policies', Policy])

    def list_policy_for_role(self, role_name):
        """
        get policy for role

        :type role_name: str
        :param role_name: The name of role

        :rtype: object
        :return: A list of  :class:`footmark.ram.policy`
        """
        params = {}
        self.build_list_params(params, role_name, 'RoleName')

        return self.get_list('ListPoliciesForRole', params, ['Policies', Policy])

    def list_policy_for_group(self, group_name):
        """
        get policy for user

        :type group_name: str
        :param group_name: The name of group

        :rtype: object
        :return: A list of  :class:`footmark.ram.policy`
        """
        params = {}
        self.build_list_params(params, group_name, 'GroupName')

        return self.get_list('ListPoliciesForGroup', params, ['Policies', Policy])

