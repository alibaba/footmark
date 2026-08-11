# encoding: utf-8
import json
from footmark.connection import ACSQueryConnection
from footmark.market.regioninfo import RegionInfo
from footmark.exception import MARKETResponseError
from footmark.market.product import Product
# from aliyunsdkmarket.request.v20151101.DescribeProductRequest import


class MARKETConnection(ACSQueryConnection):
    SDKVersion = '2015-11-01'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = MARKETResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None, alicloud_protocol=None):
        """
        Init method to create a new connection to MARKET.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.MARKETSDK = 'aliyunsdkmarket.request.v' + self.SDKVersion.replace('-', '')

        super(MARKETConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.MARKETSDK,
                                            user_agent=user_agent,
                                            ecs_role_name=ecs_role_name,
                                            alicloud_protocol=alicloud_protocol)

    def describe_products(self, **kwargs):
        query = dict(kwargs)
        page_size = query.pop('page_size', 100)
        try:
            page_size = int(page_size)
        except (TypeError, ValueError):
            raise ValueError('page_size must be an integer between 1 and 100')
        if page_size < 1 or page_size > 100:
            raise ValueError('page_size must be between 1 and 100')

        # DescribeProducts accepts values up to 100, but the Market endpoint
        # returns at most 50 records per response.  Use the effective server
        # page size for the termination condition so a request for 100 does
        # not stop after the first (50-record) response.
        page_size = min(page_size, 50)

        products = []
        page_number = 1
        while True:
            page_query = dict(query, page_size=page_size, page_number=page_number)
            page = self.get_list_new(
                self.build_request_params(self.format_request_kwargs(**page_query)),
                ['ProductItems', Product])
            products.extend(page)
            if len(page) < page_size:
                return products
            page_number += 1

    def describe_product(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Product)
