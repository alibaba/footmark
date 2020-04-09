import json
from footmark.connection import ACSQueryConnection
from footmark.exception import ROSResponseError
from aliyunsdkcore import client
from aliyunsdkcore.auth.credentials import StsTokenCredential


class ROSConnection(ACSQueryConnection):
    SDKVersion = '2019-09-10'
    DefaultRegionId = 'cn-beijing'
    DefaultRegionName = '北京'.encode("UTF-8")
    ResponseError = ROSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None):
        """
        Init method to create a new connection to ROS.
        """
        if not region:
            region = self.DefaultRegionId
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.ROSSDK = 'aliyunsdkros.request.v' + self.SDKVersion.replace('-', '')

        super(ROSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.ROSSDK,
                                            user_agent=user_agent)

    def init_connection(self):
        conn = client.AcsClient(self.acs_access_key_id, self.acs_secret_access_key, self.region,
                                user_agent=self.user_agent)

        if self.security_token:
            sts_token_credential = StsTokenCredential(self.access_key, self.secret_key, self.security_token)
            conn = client.AcsClient(region_id=self.region, user_agent=self.user_agent, credential=sts_token_credential)
        if not conn:
            raise self.FootmarkClientError('Null AcsClient ', conn)
        return conn

    def create_stack(self, stack_name, template_body, parameters, create_timeout, template_type):
        conn = self.init_connection()
        request = self.import_request('CreateStack')
        request.set_accept_format(template_type)
        request.set_StackName(stack_name)
        request.set_TimeoutInMinutes(create_timeout)
        request.set_TemplateBody(template_body)
        request.set_Parameterss(parameters)
        response = conn.do_action_with_exception(request)
        return json.loads(response, encoding='UTF-8')

    def delete_stack(self, stack_id):
        conn = self.init_connection()
        request = self.import_request('DeleteStack')
        request.set_accept_format("json")
        request.set_StackId(stack_id)
        response = conn.do_action_with_exception(request)
        return json.loads(response, encoding='UTF-8')

    def update_stack(self, stack_id, template_body, parameters, create_timeout, template_type):
        conn = self.init_connection()
        request = self.import_request('UpdateStack')
        request.set_StackId(stack_id)
        request.set_accept_format(template_type)
        request.set_TimeoutInMinutes(create_timeout)
        request.set_TemplateBody(template_body)
        request.set_Parameterss(parameters)
        response = conn.do_action_with_exception(request)
        return json.loads(response, encoding='UTF-8')

    def query_stack_id_by_name(self, stack_name, get_info=False):
        conn = self.init_connection()
        request = self.import_request('ListStacks')
        request.get_StackNames()
        response = conn.do_action_with_exception(request)
        res = json.loads(response, encoding='UTF-8') if json.loads(response, encoding='UTF-8') else None
        stacks = res.get('Stacks')
        for stack in stacks:
            if stack_name == stack.get('StackName'):
                if not get_info:
                    return stack.get('StackId')
                else:
                    return stack
        return None
