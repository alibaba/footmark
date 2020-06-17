from tests.compat import mock, unittest


class ACSMockServiceTestCase(unittest.TestCase):
    """Base class for mocking acs services."""
    # This param is used by the unittest module to display a full
    # diff when assert*Equal methods produce an error message.
    connection_class = None
    status = ''

    def setUp(self):
        self.service_connection = self.create_service_connection(
            acs_access_key_id='acs_access_key_id',
            acs_secret_access_key='acs_secret_access_key')

        self.initialize_service_connection()

    def initialize_service_connection(self):
        self.service_connection.make_request = mock.Mock()
        self.service_connection.make_request_new = mock.Mock()

    def create_service_connection(self, **kwargs):
        if self.connection_class is None:
            raise ValueError("The connection_class class attribute must be "
                             "set to a non-None value.")
        return self.connection_class(**kwargs)

    def create_response(self, status_code, header=None, body=None):
        if body is None:
            body = self.default_body()
        if header is None:
            header = [('content-length', '1343'),
                      ('access-control-allow-headers', 'X-Requested-With, X-Sequence, _aop_secret, _aop_signature'),
                      ('access-control-max-age', '172800'), ('vary', 'Accept-Encoding, Accept-Encoding'),
                      ('server', 'Tengine'),
                      ('connection', 'close'), ('date', 'Mon, 12 Sep 2016 08:30:56 GMT'),
                      ('access-control-allow-origin', '*'),
                      ('access-control-allow-methods', 'POST, GET, OPTIONS'),
                      ('content-type', 'application/json; charset=UTF-8')]

        response = [status_code, header, body]
        return response

    def set_http_response(self, status_code, header=[], body=None):
        http_response = self.create_response(status_code, header, body)
        self.service_connection.make_request.return_value = http_response
        self.service_connection.make_request_new.return_value = self.default_body()

    def default_body(self):
        return ''


class OSSMockServiceTestCase(unittest.TestCase):
    """Base class for mocking acs services."""
    # This param is used by the unittest module to display a full
    # diff when assert*Equal methods produce an error message.
    connection_class = None
    status = ''

    def setUp(self):
        self.service_connection = self.create_service_connection(
            acs_access_key_id='acs_access_key_id',
            acs_secret_access_key='acs_secret_access_key',
            bucket_name='bucket_name')

        self.initialize_service_connection()

    def initialize_service_connection(self):
        self.service_connection.make_oss_request = mock.Mock()

    def create_service_connection(self, **kwargs):
        if self.connection_class is None:
            raise ValueError("The connection_class class attribute must be "
                             "set to a non-None value.")
        return self.connection_class(**kwargs)

    def create_response(self, status_code, header=None, body=None):
        if body is None:
            body = self.default_body()
        if header is None:
            header = [('content-length', '1343'),
                      ('access-control-allow-headers', 'X-Requested-With, X-Sequence, _aop_secret, _aop_signature'),
                      ('access-control-max-age', '172800'), ('vary', 'Accept-Encoding, Accept-Encoding'),
                      ('server', 'Tengine'),
                      ('connection', 'close'), ('date', 'Mon, 12 Sep 2016 08:30:56 GMT'),
                      ('access-control-allow-origin', '*'),
                      ('access-control-allow-methods', 'POST, GET, OPTIONS'),
                      ('content-type', 'application/json; charset=UTF-8')]

        response = body
        return response

    def set_http_response(self, status_code, header=[], body=None):
        http_response = self.create_response(status_code, header, body)
        self.service_connection.make_oss_request.return_value = http_response

    def default_body(self):
        return ''
