"""
Exception classes - Subclassing allows you to check for specific errors
"""

import json

import footmark


class FootmarkClientError(Exception):
    """
    General Footmark Client error (error accessing Aliyun)
    """

    def __init__(self, reason, *args):
        super(FootmarkClientError, self).__init__(reason, *args)
        self.reason = reason

    def __repr__(self):
        return 'FootmarkClientError: %s' % self.reason

    def __str__(self):
        return 'FootmarkClientError: %s' % self.reason


class FootmarkServerError(Exception):
    def __init__(self, error=None, *args):
        Exception.__init__(self, error, *args)
        self.error = error
        self.request_id = None
        self.error_code = None
        self.message = ''
        self.http_status = ''
        if isinstance(self.error, bytes):
            try:
                self.error = error.decode('utf-8')
            except UnicodeDecodeError:
                footmark.log.debug('Unable to decode error from bytes!')

        # Attempt to parse the error response. If body isn't present,
        # then just ignore the error response.
        try:
            parsed = json.loads(self.error)
            if 'request_id' in parsed:
                self.request_id = parsed['request_id']
            if 'error_code' in parsed:
                self.error_code = parsed['error_code']
            if 'message' in parsed:
                self.message = parsed['message']
            if 'http_status' in parsed:
                self.http_status = parsed['http_status']

        except (TypeError, ValueError):
            # Remove unparsable message body so we don't include garbage
            # in exception. But first, save self.body in self.error_message
            # because occasionally we get error messages from Eucalyptus
            # that are just text strings that we want to preserve.
            self.message = self.error
            self.body = None

    def __getattr__(self, name):
        if name == 'error_message':
            return self.message
        if name == 'code':
            return self.error_code
        if name == 'status':
            return self.http_status
        raise AttributeError

    def __setattr__(self, name, value):
        if name == 'error_message':
            self.message = value
        if name == 'status':
            self.http_status = value
        super(FootmarkServerError, self).__setattr__(name, value)

    def __repr__(self):
        return '%s: %s, %s,\n%s' % (self.__class__.__name__,
                                  self.status, self.message, self.request_id)

    def __str__(self):
        return '%s: %s, %s,\n%s' % (self.__class__.__name__,
                                  self.status, self.message, self.request_id)


class ECSResponseError(FootmarkServerError):
    """
    Error in response from ECS.
    """

    def __init__(self, error=None):
        super(ECSResponseError, self).__init__(error)


class VPCResponseError(FootmarkServerError):
    """
    Error in response from VPC.
    """

    def __init__(self, status, body=None):
        super(VPCResponseError, self).__init__(status, body)


class SLBResponseError(FootmarkServerError):
    """
    Error in response from SLB.
    """

    def __init__(self, status, body=None):
        super(SLBResponseError, self).__init__(status, body)


class RDSResponseError(FootmarkServerError):
    """
    Error in response from RDS.
    """

    def __init__(self, status, body=None):
        super(RDSResponseError, self).__init__(status, body)


class OSSResponseError(FootmarkServerError):
    """
    Error in response from OSS.
    """

    def __init__(self, status, body=None):
        super(OSSResponseError, self).__init__(status, body)


class JSONResponseError(FootmarkServerError):
    """
    This exception expects the fully parsed and decoded JSON response
    body to be passed as the body parameter.

    :ivar status: The HTTP status code.
    :ivar reason: The HTTP reason message.
    :ivar body: The Python dict that represents the decoded JSON
        response body.
    :ivar error_message: The full description of the Aliyun error encountered.
    :ivar error_code: A short string that identifies the Aliyun error
        (e.g. ConditionalCheckFailedException)
    """

    def __init__(self, status, reason, body=None, *args):
        self.status = status
        self.body = body
        if self.body:
            self.error_message = self.body.get('message', None)
            self.error_code = self.body.get('__type', None)
            if self.error_code:
                self.error_code = self.error_code.split('#')[-1]
