# encoding: utf-8
import time
from footmark.connection import ACSQueryConnection
from footmark.dns.regioninfo import RegionInfo
from footmark.exception import DNSResponseError
from footmark.resultset import ResultSet
from footmark.dns.dns import Dns
from footmark.dns.group import Group
from footmark.dns.config import *
from aliyunsdkcore.acs_exception.exceptions import ServerException
# from aliyunsdkalidns.request.v20150109.AddDomainRequest import


class DNSConnection(ACSQueryConnection):
    SDKVersion = '2015-01-09'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = DNSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None):
        """
        Init method to create a new connection to DNS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.STSSDK = 'aliyunsdkalidns.request.v' + self.SDKVersion.replace('-', '')

        super(DNSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.STSSDK,
                                            user_agent=user_agent,
                                            ecs_role_name=ecs_role_name)

    def add_domain(self, **kwargs):
        domain_name = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet).domain_name
        return self.describe_domain_info(domain_name=domain_name)

    def delete_domain(self, **kwargs):
        retry = 5
        while retry:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if str(e.error_code) == "Forbbiden" or str(e.error_code).find("Dependency"):
                    time.sleep(5)
                    retry -= 1
                    continue
                raise e
        return False

    def describe_domains(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Domains', Dns])

    def describe_domain_info(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Dns)

    def update_domain_remark(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def get_main_domain_name(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Dns)

    def describe_domain_logs(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['Domains', Dns])

    def add_domain_group(self, **kwargs):
        group_id = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ResultSet).group_id
        kwargs['group_id'] = group_id
        return self.describe_domain_group(**kwargs)

    def update_domain_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def delete_domain_group(self, **kwargs):
        retry = 5
        while retry:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if str(e.error_code) == "Forbbiden" or str(e.error_code).find("Dependency"):
                    time.sleep(5)
                    retry -= 1
                    continue
                raise e
        return False

    def change_domain_group(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def describe_domain_groups(self, **kwargs):
        return self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)), ['DomainGroups', Group])

    def describe_domain_group(self, **kwargs):
        groups = self.describe_domain_groups(**kwargs)
        match = ''
        for group in groups:
            if group.group_name == kwargs['group_name']:
                match = group
        return match
