# coding:utf-8
"""
Handles basic connections to ACS
"""
import time
import footmark
import importlib
from footmark.exception import FootmarkServerError
from footmark.provider import Provider
import json
import yaml
import inspect
import base64
import uuid
from footmark.resultset import ResultSet
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import StsTokenCredential, EcsRamRoleCredential
# from aliyunsdkecs.request.v20140526.DescribeNetworkInterfacesRequest import


class ACSAuthConnection(object):
    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None, security_token=None,
                 region=None, provider='acs',  user_agent=None, ecs_role_name=None):
        """
        :keyword str acs_access_key_id: Your ACS Access Key ID (provided by
            Alicloud). If none is specified, the value in your
            ``ACS_ACCESS_KEY_ID`` environmental variable is used.
        :keyword str acs_secret_access_key: Your ACS Secret Access Key
            (provided by Alicloud). If none is specified, the value in your
            ``ACS_SECRET_ACCESS_KEY`` environmental variable is used.
        :keyword str security_token: The security token associated with
            temporary credentials issued by STS.  Optional unless using
            temporary credentials.  If none is specified, the environment
            variable ``ACS_SECURITY_TOKEN`` is used if defined.

        :keyword str region: The region ID.

        """
        self.region = region
        self.user_agent = user_agent
        if isinstance(provider, Provider):
            # Allow overriding Provider
            self.provider = provider
        else:
            self._provider_type = provider
            self.provider = Provider(self._provider_type,
                                     acs_access_key_id,
                                     acs_secret_access_key,
                                     security_token,
                                     ecs_role_name)

    def acs_access_key_id(self):
        return self.provider.access_key

    acs_access_key_id = property(acs_access_key_id)
    access_key = acs_access_key_id

    def acs_secret_access_key(self):
        return self.provider.secret_key

    acs_secret_access_key = property(acs_secret_access_key)
    secret_key = acs_secret_access_key

    def security_token(self):
        return self.provider.security_token

    security_token = property(security_token)

    def region_id(self):
        return self.region

    def ecs_role_name(self):
        return self.provider.ecs_role_name

    ecs_role_name = property(ecs_role_name)


class ACSQueryConnection(ACSAuthConnection):
    ResponseError = FootmarkServerError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None, region=None,
                 product=None, security_token=None, ecs_role_name=None, provider='acs',
                 user_agent='Alicloud-Footmark-v'+footmark.__version__):

        super(ACSQueryConnection, self).__init__(
            acs_access_key_id,
            acs_secret_access_key,
            security_token,
            ecs_role_name=ecs_role_name,
            region=region,
            provider=provider,
            user_agent=user_agent)

        self.product = product
        self.user_agent = user_agent

    def import_request(self, action):
        try:
            target = importlib.import_module(self.product + '.' + action + 'Request')
            return getattr(target, action + 'Request')()
        except Exception as e:
            raise Exception("Importing {0} request got an error: {1}.".format(action, e))

    def build_request_params(self, filters):
        action = filters['Action']
        params = {'Action': action}
        # get all of the specified request's method names dict, like {'InstanceId':'set_InstanceId', 'Name':'set_Name'}
        methods = {}
        request = self.import_request(action)
        if not request:
            raise Exception("There is no available request about action {0}.".format(action))
        for name in dir(request):
            if str(name).startswith('set_') and name[4] <= 'Z':
                methods[str(name[4:]).lower()] = name

        # build request params dict, like {'set_InstanceId':'i-12345', 'set_Name':'abcd'}
        if methods:
            for key, value in list(filters.items()):
                if value is None:
                    continue
                name = str(key).lower().replace("-", "").replace("_", "")
                if name in methods:
                    params[methods[name]] = value
        return params

    def make_request(self, action, params=None):
        conn = client.AcsClient(self.acs_access_key_id, self.acs_secret_access_key, self.region, user_agent=self.user_agent)

        if self.security_token:
            sts_token_credential = StsTokenCredential(self.access_key, self.secret_key, self.security_token)
            conn = client.AcsClient(region_id=self.region, user_agent=self.user_agent, credential=sts_token_credential)
        if not conn:
            footmark.log.error('%s %s' % ('Null AcsClient ', conn))
            raise self.FootmarkClientError('Null AcsClient ', conn)

        timeout = 200
        delay = 3
        while timeout > 0:
            try:
                request = self.import_request(action)
                request.set_accept_format('json')
                if params and isinstance(params, dict):
                    for k, v in list(params.items()):
                        if hasattr(request, k):
                            getattr(request, k)(v)
                        else:
                            request.add_query_param(k[4:], v)
                return conn.do_action_with_exception(request)
            except Exception as e:
                if str(e.error_code) == "SDK.ServerUnreachable" \
                        or str(e.message).__contains__("SDK.ServerUnreachable") \
                        or str(e.message).__contains__("Unable to connect server: timed out"):
                    time.sleep(delay)
                    timeout -= delay
                    continue
                raise e

        return None

    def build_list_params(self, params, items, label):
        if isinstance(items, str):
            items = str(items).strip()
        params['set_%s' % label] = items

    def parse_response(self, markers, body, connection):
        results = []
        body = yaml.safe_load(body)
        if not markers:
            markers = ["", ResultSet]

        result_set = ResultSet
        # For get_object
        if not markers[0] and markers[1] is not ResultSet:
            result_set = markers[1](connection)

        for key, value in list(body.items()):
            self.parse_value(value)
            setattr(result_set, self.convert_name(key), value)

        if markers[0] and markers[0] in body:
            for value in list(getattr(result_set, self.convert_name(markers[0])).values()):
                if isinstance(value, list):
                    for sub_value in value:
                        element = markers[1](connection)
                        for k, v in list(sub_value.items()):
                            setattr(element, k, v)
                        results.append(element)
                elif isinstance(value, dict):
                    element = markers[1](connection)
                    for k, v in list(value.items()):
                        setattr(element, k, v)
                    results.append(element)
                else:
                    element = markers[1](connection)
                    setattr(element, k, v)
                    results.append(element)
            return results
        return result_set

    def parse_value(self, value):
        if isinstance(value, list):
            for item in value:
                self.parse_value(item)
        if isinstance(value, dict):
            for k, v in list(value.items()):
                if isinstance(v, dict) or isinstance(v, list):
                    self.parse_value(v)
                else:
                    value.pop(k)
                    value[self.convert_name(k)] = v
            for k, v in list(value.items()):
                value.pop(k)
                value[self.convert_name(k)] = v
        # setattr(element, self.convert_name(key), value)
        return

    def convert_name(self, name):
        if name:
            new_name = ''
            tmp = ''
            for ch in name:
                if ch.isupper():
                    tmp += ch
                    continue
                if tmp:
                    ch = '_' + tmp.lower() + ch
                    tmp = ''
                new_name += ch
            if tmp:
                new_name += '_' + tmp.lower()
            if new_name.startswith('_'):
                new_name = new_name[1:]

            return new_name

    # generics
    def get_list(self, action, params, markers):
        try:
            body = self.make_request(action, params)
            footmark.log.debug('body= %s' % body)
            return self.parse_response(markers, body, self)
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise self.ResponseError(e)
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e

    def get_status(self, action, params):
        try:
            body = self.make_request(action, params)
            footmark.log.debug('body= %s' % body)
            body = json.loads(body, encoding='UTF-8')
            if body:
                return True
            return False
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise e
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e

    def get_object(self, action, params, obj):
        try:
            body = self.make_request(action, params)
            footmark.log.debug(body)
            markers = ["", obj]
            obj = self.parse_response(markers, body, self)
            if obj:
                return obj
            return None
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise e
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e

    def make_request_new(self, params):
        if not params:
            raise Exception("Request parameters should not be empty.")

        conn = None
        if self.acs_access_key_id and self.acs_secret_access_key:
            conn = client.AcsClient(self.acs_access_key_id, self.acs_secret_access_key, self.region, user_agent=self.user_agent)
            if self.security_token:
                sts_token_credential = StsTokenCredential(self.access_key, self.secret_key, self.security_token)
                conn = client.AcsClient(region_id=self.region, user_agent=self.user_agent, credential=sts_token_credential)
        else:
            if self.ecs_role_name:
                ecs_ram_role_credential = EcsRamRoleCredential(self.ecs_role_name)
                conn = client.AcsClient(region_id=self.region, user_agent=self.user_agent, credential=ecs_ram_role_credential)

        if not conn:
            footmark.log.error('%s %s' % ('Null AcsClient ', conn))
            raise self.FootmarkClientError('Null AcsClient ', conn)

        timeout = 200
        delay = 3
        if not isinstance(params, dict):
            raise Exception("Invalid request parameters: {0} should be a dict.".format(params))

        if not params.get('Action', params.get('action')):
            raise Exception("'Action' is required for this request.")

        while timeout > 0:
            request = self.import_request(params.get('Action', params.get('action')))
            request.set_accept_format('json')
            request.set_read_timeout(30)
            request.set_connect_timeout(30)
            try:
                for k, v in list(params.items()):
                    if hasattr(request, k):
                        getattr(request, k)(v)
                    else:
                        request.add_query_param(k[4:], v)
                return conn.do_action_with_exception(request)
            except ServerException as e:
                if str(e.error_code) == "SDK.ServerUnreachable" \
                        or str(e.message).__contains__("SDK.ServerUnreachable") \
                        or str(e.message).__contains__("Unable to connect server: timed out"):
                    time.sleep(delay)
                    timeout -= delay
                    continue
                raise e
            except Exception as e:
                raise e

        return None

    def convert_tags(self, tags):
        result = []
        if isinstance(tags, dict):
            for k, v in list(tags.items()):
                result.append({"Key": k, "Value": v})
        return result

    def underscore_to_studlycaps(self, text):
        """
        Convert a under_score string to studly_caps, like: aaa_bbb -> AaaBbb 
        :param text: 
        :return: 
        """
        res = ""
        for key in [_f for _f in str(text).lower().split('_') if _f]:
            res += str(key[0]).upper() + key[1:]
        return res

    def get_current_function_name(self, is_studly_caps=False):
        """
        Get the current function name and the return can be StudlyCaps.
        E.G: The current name is "aaa_bbb_ccc", if is_studly_caps, return AaaBbbCcc, else return aaa_bbb_ccc
        :param is_studly_caps: 
        :return: 
        """
        res = inspect.stack()[1][3]
        if is_studly_caps:
            return self.underscore_to_studlycaps(res)
        return res

    def build_client_token(self, prefix=None):
        client_token = str("Footmark{0}-{1}".format(prefix,uuid.uuid1()))
        if len(client_token) > 64:
            client_token = client_token[0:64]
        return client_token

    def format_request_kwargs(self, **kwargs):
        for key, value in list(kwargs.items()):
            # Format the following parameter to JSON
            if key in ["instance_ids", "disk_ids"]:
                if not value:
                    continue
                kwargs[key] = json.dumps(value)
            if key in ["page_size", "page_number"]:
                try:
                    if value and int(value):
                        kwargs[key] = json.dumps(int(value))
                    continue
                except Exception as e:
                    raise e
            # Convert Tags
            if key == "tags":
                kwargs[key] = self.convert_tags(value)

            # Base64 userdata
            if key == "user_data":
                if not value:
                    continue
                if isinstance(value, str):
                    value = value.encode('ascii')
                try:
                    if base64.b64encode(base64.b64decode(value)) != value:
                        kwargs[key] = base64.b64encode(value)
                except:
                    kwargs[key] = base64.b64encode(value)

        # Add 'Action' parameter. Using inspect.stack()[1][3] gets invoking method name
        action = self.underscore_to_studlycaps(inspect.stack()[1][3])
        if action in ["CreateInstances", "StartInstances", "StopInstances", "RebootInstances", "DeleteInstances"]:
            action = action[:-1]
        kwargs["Action"] = action

        # Add 'ClientToken' parameter
        kwargs["client_token"] = self.build_client_token(action)

        return kwargs

    def get_list_new(self, params, markers):
        try:
            body = self.make_request_new(params)
            footmark.log.debug('body= %s' % body)
            return self.parse_response(markers, body, self)
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise self.ResponseError(e)
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e

    def get_status_new(self, params):
        try:
            body = self.make_request_new(params)
            footmark.log.debug('body= %s' % body)
            body = json.loads(body, encoding='UTF-8')
            if body:
                return True
            return False
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise e
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e

    def get_object_new(self, params, obj):
        try:
            body = self.make_request_new(params)
            footmark.log.debug(body)
            markers = ["", obj]
            obj = self.parse_response(markers, body, self)
            if obj:
                return obj
            return None
        except ServerException as e:
            footmark.log.error('%s' % e)
            raise e
        except Exception as e:
            footmark.log.error('%s' % e)
            raise e
