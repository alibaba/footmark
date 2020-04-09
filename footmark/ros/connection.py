import time
from footmark.connection import ACSQueryConnection
from footmark.exception import ROSResponseError
from footmark.resultset import ResultSet
from aliyunsdkcore.acs_exception.exceptions import ServerException


class ROSConnection(ACSQueryConnection):
    SDKVersion = '2019-09-10'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")

    ResponseError = ROSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, user_agent=None, ecs_role_name=None):
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
                                            user_agent=user_agent, ecs_role_name=ecs_role_name)

    def create_stack(self, **kwargs):
        stack_id = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)),
                                       ResultSet).stack_id
        stack_info = self.get_stack(stack_id=stack_id)
        return stack_info

    def delete_stack(self, **kwargs):
        retry = 5
        while retry:
            try:
                return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
            except ServerException as e:
                if str(e.error_code) == "Forbbiden" or str(e.error_code).find("Dependency"):
                    time.sleep(5)
                    retry -= 1
                    continue
        return False

    def update_stack(self, **kwargs):
        stack_id = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)),
                                       ResultSet).stack_id
        stack_info = self.get_stack(stack_id=stack_id)
        return stack_info

    def list_stacks(self, **kwargs):
        ros_stack_objs = self.get_list_new(self.build_request_params(self.format_request_kwargs(**kwargs)),
                                           ['Stacks', ResultSet])
        if hasattr(ros_stack_objs, 'stacks') and ros_stack_objs.stacks:
            if kwargs.get('get_one'):
                return ros_stack_objs.stacks[0]
            else:
                return ros_stack_objs.stacks
        else:
            return []

    def get_stack(self, stack_id):
        ros_stack_obj = self.get_object_new(self.build_request_params(self.format_request_kwargs(stack_id=stack_id)),
                                            ResultSet)

        if ros_stack_obj:
            return {'status': ros_stack_obj.status,
                    'status_reason': ros_stack_obj.status_reason,
                    'create_time': ros_stack_obj.create_time,
                    'region_id': ros_stack_obj.region_id,
                    'disable_rollback': ros_stack_obj.disable_rollback,
                    'stack_name': ros_stack_obj.stack_name,
                    'stack_id': ros_stack_obj.stack_id,
                    'timeout_in_minutes': ros_stack_obj.timeout_in_minutes}
        else:
            return {}

