"""
This class encapsulates the provider-specific header differences.
"""


class Provider(object):
    def __init__(self, name, access_key=None, secret_key=None, security_token=None, ecs_role_name=None, profile=None,
                 shared_credentials_file=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.security_token = security_token
        self.ecs_role_name = ecs_role_name
        self.profile = profile
        self.shared_credentials_file = shared_credentials_file

    def get_access_key(self):
        # if self._credentials_need_refresh():
        #     self._populate_keys_from_metadata_server()
        return self._access_key

    def set_access_key(self, value):
        self._access_key = value

    access_key = property(get_access_key, set_access_key)

    def get_secret_key(self):
        # if self._credentials_need_refresh():
        #     self._populate_keys_from_metadata_server()
        return self._secret_key

    def set_secret_key(self, value):
        self._secret_key = value

    secret_key = property(get_secret_key, set_secret_key)

    def get_security_token(self):
        # if self._credentials_need_refresh():
        #     self._populate_keys_from_metadata_server()
        return self._security_token

    def set_security_token(self, value):
        self._security_token = value

    security_token = property(get_security_token, set_security_token)

    def get_ecs_role_name(self):
        return self._ecs_role_name

    def set_ecs_role_name(self, value):
        self._ecs_role_name = value

    ecs_role_name = property(get_ecs_role_name, set_ecs_role_name)

    def get_profile(self):
        return self._profile

    def set_profile(self, value):
        self._profile = value

    profile = property(get_profile, set_profile)

    def get_shared_credentials_file(self):
        return self._shared_credentials_file

    def set_shared_credentials_file(self, value):
        self._shared_credentials_file = value

    shared_credentials_file = property(get_shared_credentials_file, set_shared_credentials_file)


# Static utility method for getting default Provider.
def get_default():
    return Provider('acs')
