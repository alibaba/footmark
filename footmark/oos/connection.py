# encoding: utf-8
from footmark.connection import ACSQueryConnection
from footmark.oos.regioninfo import RegionInfo
from footmark.exception import OOSResponseError
from footmark.oos.oos import Template, Executions
# from aliyunsdkoos.request.v20190601.CreateTemplateRequest import


class OOSConnection(ACSQueryConnection):
    SDKVersion = '2019-06-01'
    DefaultRegionId = 'cn-hangzhou'
    DefaultRegionName = '杭州'.encode("UTF-8")
    ResponseError = OOSResponseError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, sdk_version=None, security_token=None, ecs_role_name=None, user_agent=None):
        """
        Init method to create a new connection to OOS.
        """
        if not region:
            region = RegionInfo(self, self.DefaultRegionName,
                                self.DefaultRegionId)
        self.region = region
        if sdk_version:
            self.SDKVersion = sdk_version

        self.RAMSDK = 'aliyunsdkoos.request.v' + self.SDKVersion.replace('-', '')

        super(OOSConnection, self).__init__(acs_access_key_id=acs_access_key_id,
                                            acs_secret_access_key=acs_secret_access_key,
                                            security_token=security_token,
                                            region=self.region, product=self.RAMSDK,
                                            user_agent=user_agent,
                                            ecs_role_name=ecs_role_name)

    def get_template(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Template)

    def delete_template(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def update_template(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Template)

    def list_templates(self, **kwargs):
        tmp = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Template).read()['templates']
        res = []
        if tmp:
            for t in tmp:
                elem = Template(self)
                for key, value in list(t.items()):
                    self.parse_value(value)
                    setattr(elem, self.convert_name(key), value)
                res.append(elem)
        return res

    def create_template(self, **kwargs):
        tags = kwargs.get('tags', '')
        kwargs = self.format_request_kwargs(**kwargs)
        if tags:
            kwargs['tags'] = tags
        else:
            kwargs.pop('tags')
        return self.get_object_new(self.build_request_params(kwargs), Template)

    def list_execution_risky_tasks(self, **kwargs):
        return self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Template)

    def start_execution(self, **kwargs):
        tags = kwargs.get('tags', '')
        kwargs = self.format_request_kwargs(**kwargs)
        if tags:
            kwargs['tags'] = tags
        else:
            kwargs.pop('tags')
        return self.get_object_new(self.build_request_params(kwargs), Executions)

    def cancel_execution(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def delete_executions(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_executions(self, **kwargs):
        tmp = self.get_object_new(self.build_request_params(self.format_request_kwargs(**kwargs)), Executions).read()['executions']
        res = []
        if tmp:
            for t in tmp:
                elem = Executions(self)
                for key, value in list(t.items()):
                    self.parse_value(value)
                    setattr(elem, self.convert_name(key), value)
                res.append(elem)
        return res

    def notify_execution(self, **kwargs):
        return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))

    def list_tag_resources(self, **kwargs):
        res = {}
        tags = kwargs['tags']
        kwargs = self.format_request_kwargs(**kwargs)
        kwargs['tags'] = tags
        tags = self.get_list_new(self.build_request_params(kwargs), ['TagResources', Template])
        for tag in tags:
            res[tag.tag_key] = tag.tag_value
        return res

    def tag_resources(self, **kwargs):
        tmp = {}
        if kwargs['tags']:
            for key, value in list(kwargs['tags'].items()):
                if key in list(self.list_tag_resources(**kwargs).keys()) and value == self.list_tag_resources(**kwargs)[key]:
                    continue
                tmp[key] = value
        if tmp:
            kwargs = self.format_request_kwargs(**kwargs)
            kwargs['tags'] = tmp
            return self.get_status_new(self.build_request_params(kwargs))
        return None

    def untag_resources(self, **kwargs):
        tmp = []
        if kwargs['tags']:
            for key, value in list(kwargs['tags'].items()):
                if key not in list(self.list_tag_resources(**kwargs).keys()):
                    continue
                tmp.append(key)
        if tmp:
            kwargs['tag_keys'] = tmp
            return self.get_status_new(self.build_request_params(self.format_request_kwargs(**kwargs)))
        return False
