# encoding: utf-8
"""
Represents a connection to the RAM service.
"""
import six

from footmark.connection import ACSQueryConnection
from footmark.ram.regioninfo import RegionInfo
from footmark.exception import RamResponseError
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

    def create_access_key(self,user_name,access_key_ids=None,is_active=True):
        """
        add or update access_key for user
        :type user_name: str
        :param user_name: the name of user
        :type access_key_id: str
        :param access_key_id: When update access_key's status,this field is needed
        :type is_active: bool
        :param is_active: Active or inactive the access_key
        :return: boolean value create access_key result
        """
        params = {}
        results = []
        success = False
        if user_name:
            self.build_list_params(params, user_name, 'UserName')
            if isinstance(access_key_ids, six.string_types):
                access_key_ids = [access_key_ids]
                if is_active:
                    self.build_list_params(params, 'Active', 'Status')
                else:
                    self.build_list_params(params, 'Inactive', 'Status')
                for access_key_id in access_key_ids:
                    self.build_list_params(params, access_key_id, 'UserAccessKeyId')
                    if self.get_status('UpdateAccessKey', params):
                        results.append(access_key_id)
                return results
            else:
                if self.get_status('CreateAccessKey', params):
                    success=True
                return success
        else:
            return success

    def delete_access_keys(self, user_name, access_key_ids=None):
        """
        delete access_key of user
        :type user_name: str
        :param user_name: the name of user
        :type access_key_ids: list
        :param access_key_ids: The access_keys to delete or update
        """
        params = {}
        results = []
        if user_name:
            self.build_list_params(params, user_name, 'UserName')
            if isinstance(access_key_ids, six.string_types):
                access_key_ids = [access_key_ids]
            for access_key_id in access_key_ids:
                self.build_list_params(params, access_key_id, 'UserAccessKeyId')
                if self.get_status('DeleteAccessKey', params):
                    results.append(access_key_id)
        return results

    def list_access_keys(self, user_name=None):
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
