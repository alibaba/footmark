# encoding: utf-8
"""
Represents a connection to the OSS service.
"""


from footmark.connection import ACSQueryConnection
import oss2
from footmark.exception import OSSResponseError


class OSSConnection(ACSQueryConnection):
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = u'杭州'.encode("UTF-8")
    DefaultConnectionErrorMsg = "Error in connecting to OSS. This usually occurs due to invalid region"
    ResponseError = OSSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, user_agent=None):
        """
        Init method to create a new connection to OSS.
        """
        if not region:
            region = self.DefaultRegionId

        self.region = region

        self.endpoint = "http://oss-" + self.region + ".aliyuncs.com"

        self.auth = oss2.Auth(acs_access_key_id, acs_secret_access_key)

        # self.user_agent = user_agent
        self.service = oss2.Service(self.auth, self.endpoint)

    def is_bucket_exist(self, bucket_name):
        """
        Verify if bucket exists in OSS
        :type bucket_name: str
        :param bucket_name: bucket name to verify for existence
        :rtype: bool
        :return: boolean value representing bucket existence
        """
        bucket_list = self.list_buckets(prefix=bucket_name)
        if len(bucket_list) > 0:
            return True

        return False

    def list_buckets(self, prefix=None, marker='', max_keys=100):
        """   
        List all Buckets   
        :type prefix: str
        :param prefix: prefix to search bucket
        :type marker: str
        :param marker: the key to start with when using list mode. 
          Object keys are returned in alphabetical order, starting 
          with key after the marker in order.
        :type max_keys: int
        :param max_keys: Max number of results to return in list mode
        :return: Returns list of Buckets
        """

        keys = []

        if max_keys is None:
            max_keys = 100
        response = self.service.list_buckets(prefix=prefix, marker=marker, max_keys=max_keys)

        if type(response) is oss2.models.ListBucketsResult:
            bucket_list = response.buckets
            if len(bucket_list) > 0:
                keys = [bucket_obj.name for bucket_obj in bucket_list]

        return keys

    def error_handler(self, exception):
        """

        :param exception:
        :return:
        """

        details = self.DefaultConnectionErrorMsg
        class_name = exception.__class__.__name__

        if hasattr(exception, 'details'):
            if exception.details:
                e_details = exception.details
                details = '{'
                for key in e_details:
                    details += str(key) + ": " + str(e_details[key]) + ', '

                details += '}'

        return details
