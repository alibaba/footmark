# coding:utf-8
import sys
import time

reload(sys)
sys.setdefaultencoding("utf-8")
"""
Handles basic connections to ACS
"""

import footmark
import importlib
from footmark.exception import FootmarkServerError
from footmark.provider import Provider
import json
import yaml
from footmark.resultset import ResultSet

from pprint import pprint

from aliyunsdkcore import client
from aliyunsdkcore.acs_exception.exceptions import ServerException


class ACSAuthConnection(object):
    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None,
                 region=None, provider='acs', security_token=None, user_agent=None):
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
                                     security_token)

    def acs_access_key_id(self):
        return self.provider.access_key

    acs_access_key_id = property(acs_access_key_id)
    access_key = acs_access_key_id

    def acs_secret_access_key(self):
        return self.provider.secret_key

    acs_secret_access_key = property(acs_secret_access_key)
    secret_key = acs_secret_access_key

    def region_id(self):
        return self.region


class ACSQueryConnection(ACSAuthConnection):
    ResponseError = FootmarkServerError

    def __init__(self, acs_access_key_id=None, acs_secret_access_key=None, region=None,
                 product=None, security_token=None, provider='acs',
                 user_agent='Alicloud-Footmark-v'+footmark.__version__):

        super(ACSQueryConnection, self).__init__(
            acs_access_key_id,
            acs_secret_access_key,
            region=region,
            security_token=security_token,
            provider=provider,
            user_agent=user_agent)

        self.product = product
        self.user_agent = user_agent

    def make_request(self, action, params=None):
        conn = client.AcsClient(self.acs_access_key_id, self.acs_secret_access_key, self.region, user_agent=self.user_agent)
        if not conn:
            footmark.log.error('%s %s' % ('Null AcsClient ', conn))
            raise self.FootmarkClientError('Null AcsClient ', conn)

        timeout = 200
        delay = 3
        while timeout > 0:
            try:
                target = importlib.import_module(self.product + '.' + action + 'Request')
                request = getattr(target, action + 'Request')()
                request.set_accept_format('json')
                if params and isinstance(params, dict):
                    for k, v in params.items():
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

        for key, value in body.items():
            self.parse_value(value)
            setattr(result_set, self.convert_name(key), value)

        if markers[0] and markers[0] in body:
            for value in getattr(result_set, self.convert_name(markers[0])).itervalues():
                if isinstance(value, list):
                    for sub_value in value:
                        element = markers[1](connection)
                        for k, v in sub_value.items():
                            setattr(element, k, v)
                        results.append(element)
                elif isinstance(value, dict):
                    element = markers[1](connection)
                    for k, v in value.items():
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
            for k, v in value.items():
                if isinstance(v, dict) or isinstance(v, list):
                    self.parse_value(v)
                else:
                    value.pop(k)
                    value[self.convert_name(k)] = v
            for k, v in value.items():
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
