# encoding: utf-8
"""
Represents a connection to the RAM service.
"""
import six

from footmark.connection import ACSQueryConnection
from footmark.ram.regioninfo import RegionInfo
from footmark.exception import RamResponseError
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

    def create_access_key(self,user_name):
        """
        add or update access_key for user
        :type user_name: str
        :param user_name: the name of user
        :return: create access_key result
        """
        params = {}
        access_key=None
        if user_name:
            self.build_list_params(params, user_name, 'UserName')
            result=self.get_object('CreateAccessKey', params,ResultSet)
            access_key=result.AccessKey
        return access_key

    def update_access_key(self,user_name,access_key_id=None,is_active=True):
        params = {}
        success = False
        if user_name and access_key_id:
            self.build_list_params(params, user_name, 'UserName')
            self.build_list_params(params, access_key_id, 'UserAccessKeyId')
            if is_active:
                self.build_list_params(params, 'Active', 'Status')
            else:
                self.build_list_params(params, 'Inactive', 'Status')
            success = self.get_status('UpdateAccessKey', params)
        return success

    def delete_access_keys(self, user_name, access_key_id):
        """
        delete access_key of user
        :type user_name: str
        :param user_name: the name of user
        :type access_key_id: str
        :param access_key_id: The access_key to delete
        """
        params = {}
        success = False
        if user_name:
            self.build_list_params(params, user_name, 'UserName')
            if access_key_id:
                self.build_list_params(params, access_key_id, 'UserAccessKeyId')
                success=self.get_status('DeleteAccessKey', params)
        return success

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
