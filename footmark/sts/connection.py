# encoding: utf-8
import json
from footmark.connection import ACSQueryConnection
from footmark.sts.regioninfo import RegionInfo
from footmark.exception import STSResponseError
from footmark.sts.sts import Sts
# from aliyunsdksts.request.v20150401.AssumeRoleRequest import


class STSConnection(ACSQueryConnection):
    SDKVersion = '2015-04-01'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = STSResponseError

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

        self.STSSDK = 'aliyunsdksts.request.v' + self.SDKVersion.replace('-', '')

        super(STSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.STSSDK,
                                            user_agent=user_agent,
                                            ecs_role_name=ecs_role_name)

    def format_sts_request_kwargs(self, **kwargs):
        for key, value in list(kwargs.items()):
            # format str to json
            if key == 'policy' and value:
                kwargs[key] = json.dumps(eval(value))
        return kwargs

    def assume_role(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_sts_request_kwargs(**self.format_request_kwargs(**kwargs))), Sts)

    def get_caller_identity(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_sts_request_kwargs(**self.format_request_kwargs(**kwargs))), Sts)
